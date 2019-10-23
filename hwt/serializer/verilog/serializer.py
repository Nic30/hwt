from hwt.hdl.entity import Entity
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.process import HWProcess
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.types.array import HArray
from hwt.hdl.types.typeCast import toHVal
from hwt.serializer.exceptions import SerializerException
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.mapExpr import MapExpr
from hwt.serializer.generic.nameScope import LangueKeyword
from hwt.serializer.generic.portMap import PortMap
from hwt.serializer.generic.serializer import GenericSerializer, CurrentUnitSwap
from hwt.serializer.utils import maxStmId
from hwt.serializer.verilog.context import VerilogSerializerCtx
from hwt.serializer.verilog.keywords import VERILOG_KEYWORDS
from hwt.serializer.verilog.ops import VerilogSerializer_ops
from hwt.serializer.verilog.statements import VerilogSerializer_statements
from hwt.serializer.verilog.tmplContainer import VerilogTmplContainer
from hwt.serializer.verilog.types import VerilogSerializer_types
from hwt.serializer.verilog.utils import SIGNAL_TYPE, verilogTypeOfSig
from hwt.serializer.verilog.value import VerilogSerializer_Value
from hwt.hdl.portItem import PortItem
from hwt.hdl.constants import DIRECTION
from hwt.synthesizer.param import Param
from hwt.hdl.architecture import Architecture


class VerilogSerializer(VerilogTmplContainer, VerilogSerializer_types,
                        VerilogSerializer_Value, VerilogSerializer_statements,
                        VerilogSerializer_ops, GenericSerializer):
    _keywords_dict = {kw: LangueKeyword() for kw in VERILOG_KEYWORDS}
    fileExtension = '.v'

    @classmethod
    def getBaseContext(cls):
        return VerilogSerializerCtx(cls.getBaseNameScope(), 0, None, None)

    @classmethod
    def Entity(cls, ent, ctx):
        generics, ports = cls.Entity_prepare(ent, ctx)

        entVerilog = cls.moduleHeadTmpl.render(
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
    def hardcodeRomIntoProcess(cls, rom):
        """
        Due to verilog restrictions it is not posible to use array constants
        and rom memories has to be hardcoded as process
        """
        processes = []
        signals = []
        for e in rom.endpoints:
            assert isinstance(e, Operator) and e.operator == AllOps.INDEX, e
            me, index = e.operands
            assert me is rom

            # construct output of the rom
            romValSig = rom.ctx.sig(rom.name, dtype=e.result._dtype)
            romValSig.hidden = False
            signals.append(romValSig)

            # construct process which will represent content of the rom
            cases = [(toHVal(i), [romValSig(v), ])
                     for i, v in enumerate(rom.defVal.val)]
            romSwitchStm = SwitchContainer(index, cases)

            for (_, (stm, )) in cases:
                stm.parentStm = romSwitchStm

            p = HWProcess(rom.name, [romSwitchStm, ],
                          {index, }, {index, }, {romValSig, })
            processes.append(p)

            # override usage of original index operator on rom
            # to use signal generated from this process
            for _e in e.result.endpoints:
                _e._replace_input(e.result, romValSig)
        rom.hidden = True
        return processes, signals

    @classmethod
    def Architecture_var(cls, v, serializerVars, extraTypes,
                         extraTypes_serialized, ctx, childCtx):
        """
        :return: list of extra discovered processes
        """
        t = v._dtype
        # if type requires extra definition
        if isinstance(t, HArray) and v.defVal.vld_mask:
            if v.drivers:
                raise SerializerException("Verilog does not support RAMs"
                                          " with initialized value")
            eProcs, eVars = cls.hardcodeRomIntoProcess(v)
            for _v in eVars:
                _procs = cls.Architecture_var(_v, serializerVars, extraTypes,
                                              extraTypes_serialized, ctx,
                                              childCtx)
                eProcs.extend(_procs)
            return eProcs

        v.name = ctx.scope.checkedName(v.name, v)
        serializedVar = cls.SignalItem(v, childCtx, declaration=True)
        serializerVars.append(serializedVar)

        return []

    @classmethod
    def Architecture(cls, arch: Architecture, ctx):
        serializerVars = []
        procs = []
        extraTypes = set()
        extraTypes_serialized = []
        arch.variables.sort(key=lambda x: (x.name, x._instId))
        arch.componentInstances.sort(key=lambda x: x._name)

        childCtx = ctx.withIndent()
        extraProcesses = []
        for v in arch.variables:
            _eProc = cls.Architecture_var(v,
                                          serializerVars,
                                          extraTypes,
                                          extraTypes_serialized,
                                          ctx,
                                          childCtx)

            extraProcesses.extend(_eProc)

        arch.processes.extend(extraProcesses)
        arch.processes.sort(key=lambda x: (x.name, maxStmId(x)))
        for p in arch.processes:
            p_str = cls.HWProcess(p, childCtx)
            procs.append(p_str)

        # architecture names can be same for different entities
        # arch.name = scope.checkedName(arch.name, arch, isGlobal=True)
        componentInstances = list(
            map(lambda c: cls.ComponentInstance(c, childCtx),
                arch.componentInstances))

        return cls.moduleBodyTmpl.render(
            indent=getIndent(ctx.indent),
            entityName=arch.getEntityName(),
            name=arch.name,
            variables=serializerVars,
            extraTypes=extraTypes_serialized,
            processes=procs,
            componentInstances=componentInstances
        )

    @classmethod
    def ComponentInstance(cls, entity, ctx: VerilogSerializerCtx):
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

            # [TODO] check component instance name
            return cls.componentInstanceTmpl.render(
                indent=getIndent(ctx.indent),
                instanceName=entity._name,
                entity=entity,
                portMaps=[cls.PortConnection(x, ctx) for x in portMaps],
                genericMaps=[cls.MapExpr(x, ctx) for x in genericMaps]
            )

    @classmethod
    def comment(cls, comentStr):
        return "\n".join(["/*", comentStr, "*/"])

    @classmethod
    def GenericItem(cls, g: Param, ctx):
        return ('"parameter %s = "%s"'
                % (g.hdl_name, str(g.get_value())))

    @classmethod
    def PortItem(cls, pi: PortItem, ctx):
        t = cls.HdlType(pi._dtype, ctx.forPort())
        if pi.direction == DIRECTION.IN or pi.direction == DIRECTION.INOUT:
            verilog_t = SIGNAL_TYPE.WIRE
        else:
            verilog_t = verilogTypeOfSig(pi.getInternSig())

        if verilog_t == SIGNAL_TYPE.REG:
            if t:
                f = "%s reg %s %s"
            else:
                f = "%s reg %s"
        else:
            if t:
                f = "%s %s %s"
            else:
                f = "%s %s"

        if t:
            return f % (cls.DIRECTION(pi.direction),
                        t, pi.name)
        else:
            return f % (cls.DIRECTION(pi.direction),
                        pi.name)

    @classmethod
    def PortConnection(cls, pc, ctx):
        if pc.portItem._dtype != pc.sig._dtype:
            raise SerializerException(
                "Port map %s is nod valid (types does not match)  (%s, %s)" % (
                    "%s => %s" % (pc.portItem.name, cls.asHdl(pc.sig, ctx)),
                    repr(pc.portItem._dtype), repr(pc.sig._dtype)))
        return ".%s(%s)" % (pc.portItem.name, cls.asHdl(pc.sig, ctx))

    @classmethod
    def MapExpr(cls, m: MapExpr, ctx):
        k = m.compSig
        if isinstance(k, Param):
            name = k.hdl_name
            v = '"%s"' % str(k.get_value())
        else:
            name = cls.get_signal_name(k, ctx)
            v = cls.asHdl(m.value, ctx)
        return ".%s(%s)" % (name, v)
