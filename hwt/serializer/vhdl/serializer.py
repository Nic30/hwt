import re

from hwt.hdl.entity import Entity
from hwt.hdl.types.array import HArray
from hwt.hdl.types.enum import HEnum
from hwt.pyUtils.arrayQuery import groupedby
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.mapExpr import MapExpr
from hwt.serializer.generic.nameScope import LangueKeyword, NameScope
from hwt.serializer.generic.portMap import PortMap
from hwt.serializer.generic.serializer import GenericSerializer, CurrentUnitSwap
from hwt.serializer.utils import maxStmId
from hwt.serializer.vhdl.keywords import VHLD_KEYWORDS
from hwt.serializer.vhdl.ops import VhdlSerializer_ops
from hwt.serializer.vhdl.statements import VhdlSerializer_statements
from hwt.serializer.vhdl.tmplContainer import VhdlTmplContainer
from hwt.serializer.vhdl.types import VhdlSerializer_types
from hwt.serializer.vhdl.utils import VhdlVersion
from hwt.serializer.vhdl.value import VhdlSerializer_Value
from hwt.hdl.architecture import Architecture
from hwt.synthesizer.param import Param
from hwt.hdl.portItem import PortItem


class VhdlNameScope(NameScope):
    RE_MANY_UNDERSCORES = re.compile(r"(_{2,})")

    def checkedName(self, actualName, actualObj, isGlobal=False):
        actualName = self.RE_MANY_UNDERSCORES.sub(r"_", actualName)
        return NameScope.checkedName(self, actualName, actualObj,
                                     isGlobal=isGlobal)


class VhdlSerializer(VhdlTmplContainer, VhdlSerializer_Value,
                     VhdlSerializer_ops, VhdlSerializer_types,
                     VhdlSerializer_statements, GenericSerializer):
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
    def Architecture(cls, arch: Architecture, ctx):
        with CurrentUnitSwap(ctx, arch.entity.origin):
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
                    extraTypes_serialized.append(
                        cls.HdlType(t, childCtx, declaration=True))

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

            componentInstances = list(
                map(lambda c: cls.ComponentInstance(c, childCtx),
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
        with CurrentUnitSwap(ctx, entity.origin):
            return cls.componentTmpl.render(
                indent=getIndent(ctx.indent),
                ports=[cls.PortItem(pi, ctx) for pi in entity.ports],
                generics=[cls.GenericItem(g, ctx) for g in entity.generics],
                entity=entity
            )

    @classmethod
    def ComponentInstance(cls, entity: Entity, ctx):
        with CurrentUnitSwap(ctx, entity.origin):
            portMaps = []
            for pi in entity.ports:
                pm = PortMap.fromPortItem(pi)
                portMaps.append(pm)

            genericMaps = []
            for g in entity.generics:
                gm = MapExpr(g, g.get_value())
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
    def Entity(cls, entity: Entity, ctx):
        with CurrentUnitSwap(ctx, entity.origin):
            generics, ports = cls.Entity_prepare(entity, ctx)

            entVhdl = cls.entityTmpl.render(
                indent=getIndent(ctx.indent),
                name=entity.name,
                ports=ports,
                generics=generics
            )

            doc = entity.__doc__
            if doc and id(doc) != id(Entity.__doc__):
                doc = cls.comment(doc) + "\n"
                return doc + entVhdl
            else:
                return entVhdl

    @classmethod
    def GenericItem(cls, g: Param, ctx):
        v = g.get_hdl_value()
        t_str = cls.HdlType(v._dtype, ctx)
        v_str = cls.Value(v, ctx)
        return '%s: %s := %s' % (
                g.hdl_name, t_str, v_str)

    @classmethod
    def PortConnection(cls, pc, ctx):
        if pc.portItem._dtype != pc.sig._dtype:
            raise SerializerException(
                "Port map %s is nod valid"
                " (types does not match)  (%r, %r)" % (
                    "%s => %s" % (pc.portItem.name, cls.asHdl(pc.sig, ctx)),
                    pc.portItem._dtype, pc.sig._dtype))
        return "%s => %s" % (pc.portItem.name, cls.asHdl(pc.sig, ctx))

    @classmethod
    def DIRECTION(cls, d):
        return d.name

    @classmethod
    def PortItem(cls, pi: PortItem, ctx):
        return "%s: %s %s" % (pi.name, cls.DIRECTION(pi.direction),
                              cls.HdlType(pi._dtype, ctx))

    @classmethod
    def MapExpr(cls, m: MapExpr, ctx):
        k = m.compSig
        if isinstance(k, Param):
            name = k.hdl_name
            v = cls.Value(k.get_hdl_value(), ctx)
        else:
            name = cls.get_signal_name(k, ctx)
            v = cls.asHdl(m.value, ctx)
        return "%s => %s" % (name, v)
