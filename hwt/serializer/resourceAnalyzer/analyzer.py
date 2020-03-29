from hwt.hdl.architecture import Architecture
from hwt.hdl.entity import Entity
from hwt.hdl.process import HWProcess
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.resourceAnalyzer.utils import ResourceContext
from hwt.hdl.types.array import HArray
from hwt.hdl.statements import HdlStatement
from hwt.hdl.assignment import Assignment
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.hdl.operator import Operator, isConst
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.value import Value
from hwt.synthesizer.rtlLevel.netlist import walk_assignments
from hwt.hdl.switchContainer import SwitchContainer
from itertools import chain
from hwt.doc_markers import internal


@internal
def _count_mux_inputs_for_outputs(stm: HdlStatement, cnt):
    if isinstance(stm, Assignment):
        cnt[stm.dst] += 1
    else:
        for _stm in stm._iter_stms():
            if isinstance(_stm, Assignment):
                cnt[_stm.dst] += 1
            else:
                _count_mux_inputs_for_outputs(_stm, cnt)


@internal
def count_mux_inputs_for_outputs(stm):
    cnt = {o: 0 for o in stm._outputs}
    _count_mux_inputs_for_outputs(stm, cnt)
    return cnt


IGNORED_OPERATORS = {
    AllOps.BitsAsSigned,
    AllOps.BitsAsUnsigned,
    AllOps.BitsAsVec,
    AllOps.RISING_EDGE,
    AllOps.FALLING_EDGE,
}


class ResourceAnalyzer(GenericSerializer):
    """
    Serializer which does not products any output just collect informations
    about used resources

    :attention: Use instance of ResourceAnalyzer instead of class
    """
    _keywords_dict = {}

    def __init__(self):
        self.context = ResourceContext(None)

    @internal
    @classmethod
    def HWProcess_operators(cls, sig: RtlSignal, ctx: ResourceContext, synchronous):
        seen = ctx.seen
        for d in sig.drivers:
            if (not isinstance(d, Operator)
                    or d in seen):
                continue

            skip_op = d.operator in IGNORED_OPERATORS
            if not skip_op:
                if d.operator == AllOps.EQ:
                    o1 = d.operands[1]
                    if (isinstance(o1, Value)
                            and o1._dtype.bit_length() == 1
                            and o1.val):
                        # to bool conversion
                        skip_op = True
                elif d.operator == AllOps.INDEX:
                    o1 = d.operands[1]
                    skip_op = True
                    if isConst(o1):
                        # constant signal silice
                        pass
                    else:
                        o0 = d.operands[0]
                        if isinstance(o0._dtype, HArray):
                            ctx.registerRAM_read_port(o0, o1, synchronous)
                        else:
                            ctx.registerMUX(d, sig, 2)
                elif d.operator == AllOps.TERNARY:
                    o1 = d.operands[1]
                    o2 = d.operands[2]
                    if (isConst(o1)
                            and bool(o1)
                            and isConst(o2)
                            and not bool(o2)):
                        # to bit conversion
                        skip_op = True
                    else:
                        raise NotImplementedError("Ternary as mux")

            if not skip_op:
                ctx.registerOperator(d)

            for op in d.operands:
                if (not isinstance(op, RtlSignal)
                        or not op.hidden
                        or op in seen):
                    continue
                cls.HWProcess_operators(op, ctx, synchronous)

    @classmethod
    def HWProcess(cls, proc: HWProcess, ctx: ResourceContext) -> None:
        """
        Gues resource usage by HWProcess
        """
        seen = ctx.seen
        for stm in proc.statements:
            encl = stm._enclosed_for
            full_ev_dep = stm._is_completly_event_dependent
            now_ev_dep = stm._now_is_event_dependent
            ev_dep = full_ev_dep or now_ev_dep

            out_mux_dim = count_mux_inputs_for_outputs(stm)
            for o in stm._outputs:
                if o in seen:
                    continue

                i = out_mux_dim[o]
                if isinstance(o._dtype, HArray):
                    assert i == 1, (o, i, " only one ram port per HWProcess")
                    for a in walk_assignments(stm, o):
                        assert len(a.indexes) == 1, "one address per RAM port"
                        addr = a.indexes[0]
                    ctx.registerRAM_write_port(o, addr, ev_dep)
                elif ev_dep:
                    ctx.registerFF(o)
                    if i > 1:
                        ctx.registerMUX(stm, o, i)
                elif o not in encl:
                    ctx.registerLatch(o)
                    if i > 1:
                        ctx.registerMUX(stm, o, i)
                elif i > 1:
                    ctx.registerMUX(stm, o, i)
                else:
                    # just a connection
                    continue

            if isinstance(stm, SwitchContainer):
                caseEqs = set([stm.switchOn._eq(c[0]) for c in stm.cases])
                inputs = chain(
                    [sig for sig in stm._inputs if sig not in caseEqs], [stm.switchOn])
            else:
                inputs = stm._inputs

            for i in inputs:
                # discover only internal signals in this statements for
                # operators
                if not i.hidden or i in seen:
                    continue

                cls.HWProcess_operators(i, ctx, ev_dep)

    @classmethod
    def Entity(cls, ent: Entity, ctx: ResourceContext) -> None:
        """
        Entity is just header, we do not need to inspect it for resources
        but we need to perform namechecking in order to avoid name collisions
        """
        GenericSerializer.Entity(ent, ctx)

    def getBaseContext(self) -> ResourceContext:
        """
        Return context for collecting of resource informatins
        prepared on this instance
        """
        return self.context

    @classmethod
    def Architecture(cls, arch: Architecture, ctx: ResourceContext) -> None:
        for c in arch.componentInstances:
            raise NotImplementedError()

        for proc in arch.processes:
            cls.HWProcess(proc, ctx)

        # [TODO] constant to ROMs

        ctx.finalize()

    def report(self):
        return self.context.resources
