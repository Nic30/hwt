from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.types.array import HArray
from hwt.hdlObjects.types.enum import HEnum
from hwt.hdlObjects.variables import SignalItem
from hwt.pyUtils.arrayQuery import groupedby
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.serializerClases.mapExpr import MapExpr
from hwt.serializer.serializerClases.nameScope import LangueKeyword, NameScope
from hwt.serializer.serializerClases.portMap import PortMap
from hwt.serializer.utils import maxStmId
from hwt.serializer.vhdl.keywords import VHLD_KEYWORDS
from hwt.serializer.vhdl.ops import VhdlSerializer_ops
from hwt.serializer.vhdl.statements import VhdlSerializer_statements
from hwt.serializer.vhdl.tmplContainer import VhdlTmplContainer
from hwt.serializer.vhdl.types import VhdlSerializer_types
from hwt.serializer.vhdl.utils import VhdlVersion
from hwt.serializer.vhdl.value import VhdlSerializer_Value
from hwt.synthesizer.param import getParam
import re


class DebugTmpVarStack():
    def __init__(self):
        """
        :ivar vars: list of serialized variable declarations
        """
        self.vars = []
        self.serializer = VhdlSerializer
        self.ctx = self.serializer.getBaseContext()

    def createTmpVarFn(self, suggestedName, dtype):
        # [TODO] it is better to use RtlSignal
        ser = self.serializer
        s = SignalItem(suggestedName, dtype, virtualOnly=True)
        s.hidden = False
        serializedS = ser.SignalItem(s, self.ctx, declaration=True)
        self.vars.append((serializedS, s))

        return s

    def _serializeItem(self, item):
        var, s = item
        # assignemt of value for this tmp variable
        a = Assignment(s.defaultVal, s, virtualOnly=True)
        return "%s\n%s" % (var, self.serializer.Assignment(a, self.ctx))

    def serialize(self, indent=0):
        if not self.vars:
            return ""

        separator = getIndent(indent) + "\n"
        return separator.join(map(self._serializeItem, self.vars)) + "\n"


class VhdlNameScope(NameScope):
    RE_MANY_UNDERSCORES = re.compile(r"(_{2,})")

    def checkedName(self, actualName, actualObj, isGlobal=False):
        actualName = self.RE_MANY_UNDERSCORES.sub(r"_", actualName)
        return NameScope.checkedName(self, actualName, actualObj, isGlobal=isGlobal)


class VhdlSerializer(VhdlTmplContainer, VhdlSerializer_Value,
                     VhdlSerializer_ops, VhdlSerializer_types, VhdlSerializer_statements, GenericSerializer):
    VHDL_VER = VhdlVersion.v2002
    _keywords_dict = {kw: LangueKeyword() for kw in VHLD_KEYWORDS}
    fileExtension = '.vhd'

    @classmethod
    def getBaseNameScope(cls):
        s = VhdlNameScope(True)
        s.setLevel(1)
        s[0].update(cls._keywords_dict)
        return s

    @classmethod
    def Architecture(cls, arch, ctx):
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: (x.name, x._instId))
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.components.sort(key=lambda x: x.name)
        arch.componentInstances.sort(key=lambda x: x._name)

        childCtx = ctx.withIndent()

        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, (HEnum, HArray)) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(cls.HdlType(t, childCtx, declaration=True))

            v.name = ctx.scope.checkedName(v.name, v)
            serializedVar = cls.SignalItem(v, childCtx, declaration=True)
            variables.append(serializedVar)

        for p in arch.processes:
            procs.append(cls.HWProcess(p, childCtx))

        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)

        uniqComponents = list(map(lambda x: x[1][0],
                                  groupedby(arch.components,
                                            lambda c: c.name)))
        uniqComponents.sort(key=lambda c: c.name)
        components = list(map(lambda c: cls.Component(c, childCtx),
                              uniqComponents))

        componentInstances = list(map(lambda c: cls.ComponentInstance(c, childCtx),
                                      arch.componentInstances))

        return cls.architectureTmpl.render(
            indent=getIndent(ctx.indent),
            entityName=arch.getEntityName(),
            name=arch.name,
            variables=variables,
            extraTypes=extraTypes_serialized,
            processes=procs,
            components=components,
            componentInstances=componentInstances
            )

    @classmethod
    def comment(cls, comentStr):
        return "--" + comentStr.replace("\n", "\n--")

    @classmethod
    def Component(cls, entity, ctx):
        return cls.componentTmpl.render(
                indent=getIndent(ctx.indent),
                ports=[cls.PortItem(pi, ctx) for pi in entity.ports],
                generics=[cls.GenericItem(g, ctx) for g in entity.generics],
                entity=entity
                )

    @classmethod
    def ComponentInstance(cls, entity, ctx):
        portMaps = []
        for pi in entity.ports:
            pm = PortMap.fromPortItem(pi)
            portMaps.append(pm)

        genericMaps = []
        for g in entity.generics:
            gm = MapExpr(g, g._val)
            genericMaps.append(gm)

        if len(portMaps) == 0:
            raise SerializerException("Incomplete component instance")

        entity._name = ctx.scope.checkedName(entity._name, entity)
        return cls.componentInstanceTmpl.render(
                indent=getIndent(ctx.indent),
                instanceName=entity._name,
                entity=entity,
                portMaps=[cls.PortConnection(x, ctx) for x in portMaps],
                genericMaps=[cls.MapExpr(x, ctx) for x in genericMaps]
                )

    @classmethod
    def Entity(cls, ent, ctx):
        generics, ports = cls.Entity_prepare(ent, ctx)

        entVhdl = cls.entityTmpl.render(
                indent=getIndent(ctx.indent),
                name=ent.name,
                ports=ports,
                generics=generics
                )

        doc = ent.__doc__
        if doc and id(doc) != id(Entity.__doc__):
            doc = cls.comment(doc) + "\n"
            return doc + entVhdl
        else:
            return entVhdl

    @classmethod
    def GenericItem(cls, g, ctx):
        s = "%s: %s" % (g.name, cls.HdlType(g._dtype, ctx))
        if g.defaultVal is None:
            return s
        else:
            return "%s := %s" % (s, cls.Value(getParam(g.defaultVal).staticEval(), ctx))

    @classmethod
    def PortConnection(cls, pc, ctx):
        if pc.portItem._dtype != pc.sig._dtype:
            raise SerializerException("Port map %s is nod valid (types does not match)  (%r, %r)" % (
                      "%s => %s" % (pc.portItem.name, cls.asHdl(pc.sig, ctx)),
                      pc.portItem._dtype, pc.sig._dtype))
        return "%s => %s" % (pc.portItem.name, cls.asHdl(pc.sig, ctx))

    @classmethod
    def DIRECTION(cls, d):
        return d.name

    @classmethod
    def PortItem(cls, pi, ctx):
        return "%s: %s %s" % (pi.name, cls.DIRECTION(pi.direction),
                              cls.HdlType(pi._dtype, ctx))

    @classmethod
    def MapExpr(cls, m, ctx):
        return "%s => %s" % (m.compSig.name, cls.asHdl(m.value, ctx))
