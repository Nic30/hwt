from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.enum import Enum
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.serializerClases.indent import getIndent
from hwt.serializer.serializerClases.mapExpr import MapExpr
from hwt.serializer.serializerClases.nameScope import LangueKeyword
from hwt.serializer.serializerClases.portMap import PortMap
from hwt.serializer.utils import maxStmId
from hwt.serializer.verilog.keywords import VERILOG_KEYWORDS
from hwt.serializer.verilog.ops import VerilogSerializer_ops
from hwt.serializer.verilog.statements import VerilogSerializer_statements
from hwt.serializer.verilog.templates import moduleHeadTmpl, moduleBodyTmpl, \
    componentInstanceTmpl
from hwt.serializer.verilog.types import VerilogSerializer_types
from hwt.serializer.verilog.value import VerilogSerializer_Value


class VerilogSerializer(GenericSerializer, VerilogSerializer_types, VerilogSerializer_Value, VerilogSerializer_statements, VerilogSerializer_ops):
    _keywords_dict = {kw: LangueKeyword() for kw in VERILOG_KEYWORDS}
    fileExtension = '.v'

    @classmethod
    def Entity(cls, ent, ctx):
        ports = []
        generics = []
        ent.ports.sort(key=lambda x: x.name)
        ent.generics.sort(key=lambda x: x.name)

        ent.name = ctx.scope.checkedName(ent.name, ent, isGlobal=True)
        for p in ent.ports:
            p.name = ctx.scope.checkedName(p.name, p)
            ports.append(cls.PortItem(p, ctx))

        for g in ent.generics:
            g.name = ctx.scope.checkedName(g.name, g)
            generics.append(cls.GenericItem(g, ctx))

        entVerilog = moduleHeadTmpl.render(
                indent=getIndent(ctx.indent),
                name=ent.name,
                ports=ports,
                generics=generics
                )

        doc = ent.__doc__
        if doc and id(doc) != id(Entity.__doc__):
            doc = cls.comment(doc) + "\n"
            return doc + entVerilog
        else:
            return entVerilog

    @classmethod
    def Architecture(cls, arch, ctx):
        variables = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: x.name)
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        arch.componentInstances.sort(key=lambda x: x._name)

        childCtx = ctx.withIndent()
        for v in arch.variables:
            t = v._dtype
            # if type requires extra definition
            if isinstance(t, (Enum, Array)) and t not in extraTypes:
                extraTypes.add(v._dtype)
                extraTypes_serialized.append(cls.HdlType(t, childCtx, declaration=True))

            v.name = ctx.scope.checkedName(v.name, v)
            serializedVar = cls.SignalItem(v, childCtx, declaration=True)
            variables.append(serializedVar)

        for p in arch.processes:
            procs.append(cls.HWProcess(p, childCtx))

        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)
        componentInstances = list(map(lambda c: cls.ComponentInstance(c, childCtx),
                                      arch.componentInstances))

        return moduleBodyTmpl.render(
            indent=getIndent(ctx.indent),
            entityName=arch.getEntityName(),
            name=arch.name,
            variables=variables,
            extraTypes=extraTypes_serialized,
            processes=procs,
            componentInstances=componentInstances
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

        # [TODO] check component instance name
        return componentInstanceTmpl.render(
                indent=getIndent(ctx.indent),
                instanceName=entity._name,
                entity=entity,
                portMaps=[cls.PortConnection(x, ctx) for x in portMaps],
                genericMaps=[cls.MapExpr(x, ctx) for x in genericMaps]
                )

    @classmethod
    def comment(cls, comentStr):
        return "\n".join(["/*", comentStr, "*/"])
