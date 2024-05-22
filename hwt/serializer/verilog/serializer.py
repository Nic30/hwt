from copy import copy
from typing import Optional, List

from hdlConvertorAst.hdlAst import HdlStmIf, HdlOp, \
    HdlOpType, HdlValueId, HdlModuleDec, iHdlStatement
from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlTypeAuto
from hdlConvertorAst.hdlAst._statements import HdlStmProcess, HdlStmBlock, HdlStmAssign, \
    HdlStmWait
from hdlConvertorAst.to.verilog.keywords import IEEE1800_2017_KEYWORDS
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword, NameScope
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.types.array import HArray
from hwt.hdl.types.defs import STR, INT, BOOL
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.verilog.context import SignalTypeSwap
from hwt.serializer.verilog.ops import ToHdlAstVerilog_ops
from hwt.serializer.verilog.statements import ToHdlAstVerilog_statements
from hwt.serializer.verilog.types import ToHdlAstVerilog_types
from hwt.serializer.verilog.utils import SIGNAL_TYPE, verilogTypeOfSig
from hwt.serializer.verilog.value import ToHdlAstVerilog_Value


class ToHdlAstVerilog(ToHdlAstVerilog_types,
                      ToHdlAstVerilog_Value, ToHdlAstVerilog_statements,
                      ToHdlAstVerilog_ops, ToHdlAst):
    _keywords_dict = {kw: LanguageKeyword() for kw in IEEE1800_2017_KEYWORDS}

    def __init__(self, name_scope: Optional[NameScope]=None):
        ToHdlAst.__init__(self, name_scope=name_scope)
        self.signalType = SIGNAL_TYPE.PORT_WIRE

    def as_hdl_HdlModuleDef_variable(
            self, v, types, hdl_types, hdl_variables,
            processes, component_insts):
        new_v = copy(v)
        with SignalTypeSwap(self, verilogTypeOfSig(v.origin)):
            t = v.type
            # if type requires extra definition
            if self.does_type_requires_extra_def(t, types):
                _t = self.as_hdl_HdlType(t, declaration=True)
                hdl_types.append(_t)
                types.add(t)
            new_v.type = self.as_hdl_HdlType(t, declaration=False)
            # this is a array variable which requires value intialization in init
            # process
            if isinstance(t, HArray):
                if v.value.vld_mask:
                    rom = v.origin
                    p = HdlStmProcess()
                    label = self.name_scope.checked_name(rom._name + "_rom_init", p)
                    p.labels.append(label)
                    p.body = HdlStmBlock()
                    body = p.body.body
                    for i, _v in enumerate(rom.def_val):
                        a = HdlStmAssign(self.as_hdl_int(int(_v)),
                                         self.as_hdl(rom[i]))
                        a.is_blocking = True
                        body.append(a)
                    w = HdlStmWait()
                    w.val = []  # initial process
                    body.append(w)
                    processes.append(p)
                # because we would not be able to initialize const/localparam variable later
                new_v.is_const = False
                new_v.value = None
            elif new_v.value is not None:
                if new_v.value.vld_mask:
                    new_v.value = self.as_hdl_Value(new_v.value)
                else:
                    # 'x' is a default value no need to specify it extra
                    new_v.value = None
            return new_v

    def _static_assert_false(self, msg:str):
        return hdl_call(HdlValueId("$error"), [f"%m {msg:s}"])

    def _static_assert_symbol_eq(self, symbol_name:str, v):
        i = HdlStmIf()
        i.in_preproc = True
        # [TODO] this actually requires SV>=2009
        # generate
        # if (p==x) begin
        #     $error("%m Generated only for this param value");
        # end
        # endgenerate
        i.cond = HdlOp(HdlOpType.NE, [HdlValueId(symbol_name), v])
        i.if_true = hdl_call(HdlValueId("$error"), [
             "%m Generated only for this param value",
             ])
        return i

    def as_hdl_GenericItem(self, g: HdlIdDef):
        with SignalTypeSwap(self, SIGNAL_TYPE.PORT_WIRE):
            new_v = copy(g)
            v = g.value
            if v._dtype == STR or v._dtype == INT or v._dtype == BOOL:
                t = HdlTypeAuto
            else:
                t = self.as_hdl_HdlType(v._dtype)
            new_v.type = t
            assert new_v.value is not None, g
            new_v.value = self.as_hdl_Value(v)
            return new_v

    def as_hdl_HdlPortItem(self, pi: HdlPortItem):
        with SignalTypeSwap(self, verilogTypeOfSig(pi)):
            v = super(ToHdlAstVerilog, self).as_hdl_HdlPortItem(pi)
            v.is_latched = self.signalType == SIGNAL_TYPE.PORT_REG
        return v

    def _as_hdl_HdlModuleDef_param_asserts(self, new_m: HdlModuleDec) -> List[iHdlStatement]:
        return ToHdlAst._as_hdl_HdlModuleDef_param_asserts_real(self, new_m)
