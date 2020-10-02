from copy import copy
from itertools import chain
from typing import Tuple

from hdlConvertorAst.hdlAst._bases import iHdlStatement
from hdlConvertorAst.hdlAst._statements import HdlStmBlock
from hdlConvertorAst.hdlAst._structural import HdlModuleDef, HdlCompInst
from hwt.hdl.assignment import Assignment
from hwt.hdl.block import HdlStatementBlock
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.switchContainer import SwitchContainer
from hwt.serializer.combLoopAnalyzer.tarjan import StronglyConnectedComponentSearchTarjan
from hwt.serializer.resourceAnalyzer.analyzer import ResourceAnalyzer
from hwt.synthesizer.componentPath import ComponentPath
from hwt.synthesizer.unit import Unit
from ipCorePackager.constants import DIRECTION


def collect_comb_inputs(ctx, seen, input_signal, comb_inputs):
    if input_signal not in seen:
        seen.add(input_signal)
        input_signal._walk_sensitivity(comb_inputs, seen, ctx)


def collect_comb_drivers(path_prefix: Tuple[Unit, ...],
                         stm: iHdlStatement,
                         comb_connection_matrix: dict,
                         comb_inputs: tuple):
    if isinstance(stm, Assignment):
        ctx = SensitivityCtx()
        seen = set()
        # merge condition inputs to current_comb_inputs
        current_comb_inputs = set(comb_inputs)
        for inp in stm._inputs:
            collect_comb_inputs(ctx, seen, inp, current_comb_inputs)

        for o in stm._outputs:
            o_key = path_prefix / o
            for i in current_comb_inputs:
                con = comb_connection_matrix.setdefault(path_prefix / i, set())
                con.add(o_key)

    elif isinstance(stm, IfContainer):
        current_comb_inputs = set(comb_inputs)  # intended copy
        elifs = ((stm.cond, stm.ifTrue), *stm.elIfs)
        ev_dep_branch = stm._event_dependent_from_branch
        ctx = SensitivityCtx()
        seen = set()
        found_event_dep = False
        for branch_i, (cond, stms) in enumerate(elifs):
            # [TODO] check if this works for clock gating
            if ev_dep_branch is not None and ev_dep_branch == branch_i:
                found_event_dep = True
                break

            collect_comb_inputs(ctx, seen, cond, current_comb_inputs)

            for sub_stm in stms:
                collect_comb_drivers(path_prefix, sub_stm, comb_connection_matrix, current_comb_inputs)

        if not found_event_dep and stm.ifFalse is not None:
            for sub_stm in stms:
                collect_comb_drivers(path_prefix, sub_stm, comb_connection_matrix, current_comb_inputs)           

    elif isinstance(stm, HdlStatementBlock):
        for sub_stm in stm.statements:
            collect_comb_drivers(path_prefix, sub_stm, comb_connection_matrix, comb_inputs)

    elif isinstance(stm, SwitchContainer):
        current_comb_inputs = set(comb_inputs) 
        ctx = SensitivityCtx()
        seen = set()
        collect_comb_inputs(ctx, seen, stm.switchOn, current_comb_inputs)
        cases = stm.cases
        if stm.default is not None:
            cases = chain(cases, ((None, stm.default),))
            
        for (_, case_stms) in cases:
            for sub_stm in case_stms:
                collect_comb_drivers(path_prefix, sub_stm, comb_connection_matrix, current_comb_inputs)

    else:
        raise NotImplementedError(stm)
    
    
class CombLoopAnalyzer():
    """
    Visitor which can walk synthetized hwt Unit instances and detect clusters connected by combinational logic 
    """

    def __init__(self):
        # RtlSignal: Set[RtlSignal]
        self.comb_connection_matrix = {}
        # RtlSignal: set of signals in comb loop
        self._report = {}
        self.actual_path_prefix = ComponentPath()

    def visit_Unit(self, u: Unit):
        if u._shared_component_with is None:
            arch = u._ctx.arch
        else:
            _u, _, _ = u._shared_component_with
            arch = _u._ctx.arch
        assert arch is not None, u

        self.visit_HdlModuleDef(arch)

    def visit_HdlModuleDef(self, m: HdlModuleDef) -> None:
        ResourceAnalyzer.visit_HdlModuleDef(self, m)

    def visit_HdlStatementBlock(self, proc: HdlStatementBlock) -> None:
        collect_comb_drivers(self.actual_path_prefix, proc, self.comb_connection_matrix, tuple())
    
    def visit_HdlCompInst(self, o: HdlCompInst) -> None:
        orig_path_prefix = self.actual_path_prefix 
        in_component_path_prefix = orig_path_prefix
        if o.origin._shared_component_with is not None:
            in_component_path_prefix = in_component_path_prefix / o.origin
         

        try:
            assert o.origin, o
            self.actual_path_prefix = in_component_path_prefix
            self.visit_Unit(o.origin)

            for pm in o.port_map:
                if pm.direction == DIRECTION.OUT:
                    k = in_component_path_prefix / pm.src
                    v = orig_path_prefix / pm.dst
                elif pm.direction == DIRECTION.IN:
                    k = orig_path_prefix / pm.src
                    v = in_component_path_prefix / pm.dst
                else:
                    raise NotImplementedError(pm.direction)
                self.comb_connection_matrix.setdefault(k, set()).add(v)

        finally:
            self.actual_path_prefix = orig_path_prefix

    def report(self):
        scc_search = StronglyConnectedComponentSearchTarjan(self.comb_connection_matrix)
        for scc in scc_search.search_strongly_connected_components():
            if len(scc) > 1:
                yield scc
