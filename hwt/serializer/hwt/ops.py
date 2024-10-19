from hdlConvertorAst.hdlAst._expr import HdlOp, HdlValueId
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_getattr, \
    hdl_call
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.serializer.hwt.context import ValueWidthRequirementScope
from hwt.serializer.simModel.value import ToHdlAstSimModel_value


class ToHdlAstHwt_ops():
    CONVERT_UNKNOWN_OPS_TO_FN_CALL = False
    CONCAT = HdlValueId("Concat", obj=LanguageKeyword())
    op_transl_dict = ToHdlAstSimModel_value.op_transl_dict
    _cast_ops = ToHdlAstSimModel_value._cast_ops

    def as_hdl_HOperatorNode(self, op: HOperatorNode):
        ops = op.operands
        o = op.operator

        with ValueWidthRequirementScope(self, o == HwtOps.CONCAT):
            if o in self._cast_ops:
                op0 = hdl_getattr(self.as_hdl(ops[0]), "_reinterpret_cast")
                op1 = self.as_hdl_HdlType(op.result._dtype)
                return hdl_call(op0, [op1, ])
            elif o == HwtOps.EQ:
                return hdl_call(hdl_getattr(self.as_hdl(ops[0]), "_eq"),
                                [self.as_hdl(ops[1])])
            elif o == HwtOps.CONCAT:
                return hdl_call(self.CONCAT,
                                [self.as_hdl(o2) for o2 in ops])
            elif o == HwtOps.TERNARY:
                cond, op0, op1 = ops
                cond = self.as_hdl(cond)
                with ValueWidthRequirementScope(self, True):
                    op0 = self.as_hdl(op0)
                    op1 = self.as_hdl(op1)
                return hdl_call(hdl_getattr(cond, "_ternary"), [op0, op1])
            else:

                _o = self.op_transl_dict.get(o, None)
                if self.CONVERT_UNKNOWN_OPS_TO_FN_CALL:
                    if _o is None:
                        return hdl_call(HdlValueId(o.id, obj=o._evalFn),
                                        [self.as_hdl(o2) for o2 in ops])

                assert _o is not None, o
                return HdlOp(_o, [self.as_hdl(o2)
                                 for o2 in ops])
