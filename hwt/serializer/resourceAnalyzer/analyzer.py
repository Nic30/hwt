from itertools import chain

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._structural import HdlModuleDef, \
    HdlCompInst
from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode, isConst
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.codeBlockContainer import HdlStmCodeBlockContainer
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.statements.switchContainer import SwitchContainer
from hwt.hdl.types.array import HArray
from hwt.serializer.resourceAnalyzer.utils import ResourceContext
from hwt.hwModule import HwModule
from hwt.synthesizer.rtlLevel.mark_visibility_of_signals_and_check_drivers import walk_assignments
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


@internal
def _count_mux_inputs_for_outputs(stm: HdlStatement, cnt):
    if isinstance(stm, HdlAssignmentContainer):
        cnt[stm.dst] += 1
    else:
        for _stm in stm._iter_stms():
            if isinstance(_stm, HdlAssignmentContainer):
                cnt[_stm.dst] += 1
            else:
                _count_mux_inputs_for_outputs(_stm, cnt)


@internal
def count_mux_inputs_for_outputs(stm):
    cnt = {o: 0 for o in stm._outputs}
    _count_mux_inputs_for_outputs(stm, cnt)
    return cnt


# operators which do not consume a hw resorce directly
IGNORED_OPERATORS = {
    HwtOps.BitsAsSigned,
    HwtOps.BitsAsUnsigned,
    HwtOps.BitsAsVec,
    HwtOps.RISING_EDGE,
    HwtOps.FALLING_EDGE,
}


class ResourceAnalyzer():
    """
    Serializer which does not products any output just collect informations
    about used resources

    :attention: Use instance of ResourceAnalyzer instead of class
    """
    _keywords_dict = {}

    def __init__(self):
        self.context = ResourceContext(None)

    @internal
    def visit_HdlStmCodeBlockContainer_operators(self, sig: RtlSignal, synchronous):
        ctx = self.context
        seen = ctx.seen
        for d in sig._rtlDrivers:
            if (not isinstance(d, HOperatorNode)
                    or d in seen):
                continue

            skip_op = d.operator in IGNORED_OPERATORS
            if not skip_op:
                if d.operator == HwtOps.EQ:
                    o1 = d.operands[1]
                    if (isinstance(o1, HConst)
                            and o1._dtype.bit_length() == 1
                            and o1.val):
                        # to bool conversion
                        skip_op = True
                elif d.operator == HwtOps.INDEX:
                    o1 = d.operands[1]
                    skip_op = True
                    if isConst(o1):
                        # constant signal slice
                        pass
                    else:
                        o0 = d.operands[0]
                        if isinstance(o0._dtype, HArray):
                            ctx.registerRAM_read_port(o0, o1, synchronous)
                        else:
                            ctx.registerMUX(d, sig, 2)
                elif d.operator == HwtOps.TERNARY:
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
                        or not op._isUnnamedExpr
                        or op in seen):
                    continue
                self.visit_HdlStmCodeBlockContainer_operators(op, synchronous)

    def visit_HdlStmCodeBlockContainer(self, proc: HdlStmCodeBlockContainer) -> None:
        """
        Guess resource usage from HdlStmCodeBlockContainer
        """
        ctx = self.context
        seen = ctx.seen
        for stm in proc.statements:
            encl = stm._enclosed_for
            full_ev_dep = stm._event_dependent_from_branch == 0
            now_ev_dep = stm._event_dependent_from_branch is not None
            ev_dep = full_ev_dep or now_ev_dep

            out_mux_dim = count_mux_inputs_for_outputs(stm)
            for o in stm._outputs:
                if o in seen:
                    continue

                i = out_mux_dim[o]
                if isinstance(o._dtype, HArray):
                    assert i == 1, (o, i, " only one ram port per HdlStmCodeBlockContainer")
                    for a in walk_assignments(stm, o):
                        assert len(a.indexes) == 1, ("has to have single address per RAM port", a.indexes)
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
                if not i._isUnnamedExpr or i in seen:
                    continue

                self.visit_HdlStmCodeBlockContainer_operators(i, ev_dep)

    def visit_HdlModuleDef(self, m: HdlModuleDef) -> None:
        for o in m.objs:
            if isinstance(o, HdlStmCodeBlockContainer):
                self.visit_HdlStmCodeBlockContainer(o)
            elif isinstance(o, HdlCompInst):
                self.visit_HdlCompInst(o)
            else:
                assert isinstance(o, HdlIdDef), o

    def visit_HdlCompInst(self, o: HdlCompInst) -> None:
        raise NotImplementedError()

    # [TODO] constant to ROMs
    def visit_HwModule(self, m: HwModule):
        self.visit_HdlModuleDef(m._rtlCtx.hwModDef)

    def report(self):
        ctx = self.context
        ctx.finalize()
        return ctx.resources
