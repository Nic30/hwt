from copy import copy
from typing import Optional, List

from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlValueInt, HdlOp,\
    HdlOpType
from hdlConvertorAst.hdlAst._statements import HdlStmIf, HdlStmAssign,\
    HdlStmProcess, HdlStmBlock
from hdlConvertorAst.hdlAst._structural import HdlModuleDec, HdlModuleDef
from hdlConvertorAst.to.basic_hdl_sim_model.keywords import SIMMODEL_KEYWORDS
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_getattr,\
    hdl_map_asoc, hdl_call
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.hdl.assignment import Assignment
from hwt.hdl.block import HdlStatementBlock
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.switchContainer import SwitchContainer
from hwt.serializer.generic.constant_cache import ConstantCache
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.simModel.types import ToHdlAstSimModel_types
from hwt.serializer.simModel.value import ToHdlAstSimModel_value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pycocotb.basic_hdl_simulator.sim_utils import sim_eval_cond


class ToHdlAstSimModel(ToHdlAstSimModel_value, ToHdlAstSimModel_types,
                       ToHdlAst):
    """
    Serializer which converts Unit instances to simulator code
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in SIMMODEL_KEYWORDS}
    SIM_EVAL_COND = HdlValueId("sim_eval_cond", obj=sim_eval_cond)
    C = HdlValueId("c", obj=LanguageKeyword())
    CVLD = HdlValueId("cVld", obj=LanguageKeyword())

    def __init__(self, name_scope: Optional[NameScope] = None):
        super(ToHdlAstSimModel, self).__init__(name_scope)
        self.currentUnit = None
        self.stm_outputs = {}

    def as_hdl_HdlModuleDec(self, o: HdlModuleDec):
        # convert types, exprs
        # delete params because they should not be used in expressions and thus
        # are useless
        new_o = copy(o)
        new_o.params = []
        new_o.ports = [self.as_hdl_HdlPortItem(p) for p in o.ports]
        return new_o

    def as_hdl_PortConnection(self, o: HdlPortItem):
        assert isinstance(o, HdlPortItem), o
        intern, outer = o.getInternSig(), o.getOuterSig()
        assert not intern.hidden, intern
        assert not outer.hidden, outer
        intern_hdl = HdlValueId(intern.name, obj=intern)
        outer_hdl = HdlValueId(outer.name, obj=outer)
        pm = hdl_map_asoc(intern_hdl, outer_hdl)
        return pm

    def as_hdl_Assignment(self, a: Assignment):
        dst, dst_indexes, src = self._as_hdl_Assignment_auto_conversions(a)
        ev = HdlValueInt(int(a._event_dependent_from_branch == 0), None, None)
        if dst_indexes is not None:
            src = (src, dst_indexes, ev)
        else:
            src = (src, ev)
        hdl_dst = hdl_getattr(hdl_getattr(self.SELF_IO, dst.name), "val_next")
        hdl_a = HdlStmAssign(src, hdl_dst)
        hdl_a.is_blocking = dst.virtual_only
        return hdl_a

    def as_hdl_IfContainer_out_invalidate_section(self,
                                                  outputs: List[RtlSignalBase],
                                                  parent: IfContainer):
        outputInvalidateStms = []
        for o in outputs:
            # [TODO] look up indexes
            indexes = None
            v = o._dtype.from_py(None)
            oa = Assignment(v, o, indexes,
                            virtual_only=True, parentStm=parent,
                            event_dependent_from_branch=parent._event_dependent_from_branch)
            outputInvalidateStms.append(self.as_hdl_Assignment(oa))

        if len(outputInvalidateStms) == 1:
            return outputInvalidateStms[0]
        else:
            b = HdlStmBlock()
            b.body = outputInvalidateStms
            return b

    def as_hdl_IfContainer_cond_eval(self, cond):
        """
        constructs condition evaluation statement
        c, cVld = sim_eval_cond(cond)
        """
        c, cVld = self.C, self.CVLD
        cond = self.as_hdl_cond(cond, True)
        cond_eval = hdl_call(self.SIM_EVAL_COND, [cond])
        cond_eval = HdlStmAssign(cond_eval, (c, cVld))
        cond_eval.is_blocking = True
        return c, cVld, cond_eval

    def as_hdl_IfContainer(self, ifc: IfContainer) -> HdlStmIf:
        """
        .. code-block:: python

            if cond:
                ...
            else:
                ...

        will become

        .. code-block:: python

            c, cVld = sim_eval_cond(cond)
            if not cVld:
                # ivalidate outputs
            elif c:
                ... # original if true branch
            else:
                ... # original if else brach
        """
        invalidate_block = self.as_hdl_IfContainer_out_invalidate_section(
            ifc._outputs, ifc)
        c, cVld, cond_eval = self.as_hdl_IfContainer_cond_eval(ifc.cond)
        _if = HdlStmIf()
        res = HdlStmBlock()
        res.body = [cond_eval, _if]

        _if.cond = HdlOp(HdlOpType.NEG_LOG, [cVld, ])
        _if.if_true = invalidate_block

        if_true = self.as_hdl_statements(ifc.ifTrue)
        _if.elifs.append((c, if_true))
        elifs = iter(ifc.elIfs)
        for eif_c, eif_stms in elifs:
            c, cVld, cond_eval = self.as_hdl_IfContainer_cond_eval(eif_c)
            newIf = HdlStmIf()
            newIf.cond = HdlOp(HdlOpType.NEG_LOG, [cVld, ])
            newIf.if_true = invalidate_block

            if_true = self.as_hdl_statements(eif_stms)
            newIf.elifs.append((c, if_true))

            _if.if_false = HdlStmBlock()
            _if.if_false.body = [cond_eval, newIf]
            _if = newIf

        _if.if_false = self.as_hdl_statements(ifc.ifFalse)

        return res

    def as_hdl_SwitchContainer(self, sw: SwitchContainer) -> HdlStmIf:
        "switch -> if"
        switchOn = sw.switchOn

        def mkCond(c):
            return switchOn._eq(c)

        elIfs = []

        for key, statements in sw.cases[1:]:
            elIfs.append((mkCond(key), statements))
        ifFalse = sw.default

        topCond = mkCond(sw.cases[0][0])
        topIf = IfContainer(topCond,
                            ifTrue=sw.cases[0][1],
                            ifFalse=ifFalse,
                            elIfs=elIfs)

        topIf._sensitivity = sw._sensitivity
        topIf._inputs = sw._inputs
        topIf._outputs = sw._outputs

        return self.as_hdl_IfContainer(topIf)

    def sensitivityListItem(self, item, anyEventDependent):
        if isinstance(item, Operator):
            op = item.operator
            if op == AllOps.RISING_EDGE:
                sens = HdlOpType.RISING
            elif op == AllOps.FALLING_EDGE:
                sens = HdlOpType.FALLING
            else:
                raise TypeError("This is not an event sensitivity", op)

            return HdlOp(sens, [HdlValueId(item.operands[0].name)])
        else:
            return HdlValueId(item.name)

    def has_to_be_process(self, proc):
        return True

    def can_pop_process_wrap(self, statements, hasToBeVhdlProcess):
        return False

    def as_hdl_HdlStatementBlock(self, proc: HdlStatementBlock) -> HdlStmProcess:
        p = ToHdlAst.as_hdl_HdlStatementBlock(self, proc)
        self.stm_outputs[p] = sorted(
            [HdlValueId(i.name, obj=i)
             for i in proc._outputs]
        )
        return p

    def as_hdl_extraVarsInit(self, extraVars):
        return []

    def _as_hdl_HdlModuleDef_body(self, *args) -> HdlModuleDef:
        orig_const_cache = self.constCache
        try:
            self.constCache = ConstantCache(self.createTmpVarFn)
            return ToHdlAst._as_hdl_HdlModuleDef_body(self, *args)
        finally:
            self.constCache = orig_const_cache
