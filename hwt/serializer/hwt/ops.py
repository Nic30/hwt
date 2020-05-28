from hdlConvertorAst.hdlAst._expr import HdlOpType, HdlOp, HdlValueId
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_getattr,\
    hdl_call
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.serializer.generic.ops import HWT_TO_HDLCONVEROTR_OPS
from hwt.serializer.hwt.context import ValueWidthRequirementScope


class ToHdlAstHwt_ops():
    CONCAT = HdlValueId("Concat", obj=LanguageKeyword())
    op_transl_dict = {
        **HWT_TO_HDLCONVEROTR_OPS,
        AllOps.INDEX: HdlOpType.INDEX,
    }
    _cast_ops = {
        AllOps.BitsAsSigned,
        AllOps.BitsAsUnsigned,
        AllOps.BitsAsVec,
    }

    def as_hdl_Operator(self, op: Operator):
        ops = op.operands
        o = op.operator

        with ValueWidthRequirementScope(self, o == AllOps.CONCAT):
            if o in self._cast_ops:
                op0 = hdl_getattr(self.as_hdl(ops[0]), "_reinterpret_cast")
                op1 = self.as_hdl_HdlType(op.result._dtype)
                return hdl_call(op0, [op1, ])
            elif o == AllOps.EQ:
                return hdl_call(hdl_getattr(self.as_hdl(ops[0]), "_eq"),
                                [self.as_hdl(ops[1])])
            elif o == AllOps.CONCAT:
                return hdl_call(self.CONCAT,
                                [self.as_hdl(o2) for o2 in ops])
            elif o == AllOps.TERNARY:
                cond, op0, op1 = ops
                cond = self.as_hdl(cond)
                with ValueWidthRequirementScope(self, True):
                    op0 = self.as_hdl(op0)
                    op1 = self.as_hdl(op1)
                return hdl_call(hdl_getattr(cond, "_ternary"), [op0, op1])
            else:
                o = self.op_transl_dict[o]
                return HdlOp(o, [self.as_hdl(o2)
                                 for o2 in ops])
