from typing import Union

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOp, HdlOpType
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call,\
    hdl_getattr
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.code import Concat
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.value import HValue
from hwt.hdl.variables import SignalItem
from hwt.serializer.generic.ops import HWT_TO_HDLCONVEROTR_OPS
from hwt.serializer.generic.value import ToHdlAst_Value
from pyMathBitPrecise.array3t import Array3val
from pyMathBitPrecise.bits3t import Bits3val, Bits3t


class ToHdlAstSimModel_value(ToHdlAst_Value):
    Bits3val = HdlValueId("Bits3val", obj=Bits3val)
    Bits3t = HdlValueId("Bits3t", obj=Bits3t)
    SELF = HdlValueId("self", obj=LanguageKeyword())
    Array3val = HdlValueId("Array3val", obj=Array3val)
    SLICE = HdlValueId("slice", obj=slice)
    TRUE = HdlValueId("True", obj=True)
    FALSE = HdlValueId("False", obj=False)
    Bits3val = HdlValueId("Bits3val", obj=Bits3val)
    ABits3t = HdlValueId("Bits3t", obj=Bits3t)
    SELF_IO = hdl_getattr(HdlValueId("self", obj=LanguageKeyword()), "io")
    CONCAT = HdlValueId("Concat", obj=Concat)
    op_transl_dict = {
        **HWT_TO_HDLCONVEROTR_OPS,
        AllOps.INDEX: HdlOpType.INDEX,
    }

    def is_suitable_for_const_extract(self, val: HValue):
        return not isinstance(val._dtype, HEnum) or val.vld_mask == 0

    def as_hdl_SignalItem(self, si: Union[SignalItem, HdlIdDef],
                          declaration=False):
        if not declaration and not si.hidden:
            if si._const:
                return hdl_getattr(self.SELF, si.name)
            else:
                return hdl_getattr(hdl_getattr(self.SELF_IO, si.name), "val")
        else:
            return super(ToHdlAstSimModel_value, self).as_hdl_SignalItem(
                si, declaration=declaration)

    def as_hdl_BitsVal(self, val: BitsVal):
        dtype = val._dtype
        as_hdl_int = self.as_hdl_int
        t = hdl_call(self.Bits3t, [
            as_hdl_int(dtype.bit_length()), as_hdl_int(int(bool(dtype.signed)))])
        return hdl_call(self.Bits3val, [t,
                                        as_hdl_int(val.val),
                                        as_hdl_int(val.vld_mask)])

    def as_hdl_DictVal(self, val):
        return {
            self.as_hdl_int(int(k)): self.as_hdl_Value(v)
            for k, v in val.items()
        }

    def as_hdl_HArrayVal(self, val):
        return hdl_call(self.Array3val, [
            self.as_hdl_HdlType(val._dtype),
            self.as_hdl_DictVal(val.val),
            self.as_hdl_int(val.vld_mask)
        ])

    def as_hdl_SliceVal(self, val):
        args = (
            val.val.start,
            val.val.stop,
            val.val.step
        )
        return hdl_call(self.SLICE, [self.as_hdl_int(int(a)) for a in args])

    def as_hdl_HEnumVal(self, val: HEnumVal):
        t_name = self.name_scope.get_object_name(val._dtype)
        if val.vld_mask:
            name = self.name_scope.get_object_name(val)
            return hdl_getattr(hdl_getattr(self.SELF, t_name), name)
        else:
            return hdl_call(hdl_getattr(hdl_getattr(self.SELF, t_name), "from_py"),
                            [None, ])

    def as_hdl_Operator(self, op: Operator):
        ops = op.operands
        o = op.operator

        if o == AllOps.EQ:
            op0 = self.as_hdl_Value(ops[0])
            op1 = self.as_hdl_Value(ops[1])
            return hdl_call(hdl_getattr(op0, "_eq"), [op1, ])
        elif o == AllOps.TERNARY:
            zero, one = BIT.from_py(0), BIT.from_py(1)
            if ops[1] == one and ops[2] == zero:
                # ignore redundant x ? 1 : 0
                return self.as_hdl_cond(ops[0], True)
            else:
                op0 = self.as_hdl_cond(ops[0], True)
                op1 = self.as_hdl_Value(ops[1])
                op2 = self.as_hdl_Value(ops[2])
                return hdl_call(hdl_getattr(op0, "_ternary"), [op1, op2])
        elif o == AllOps.RISING_EDGE or o == AllOps.FALLING_EDGE:
            if o == AllOps.RISING_EDGE:
                fn = "_onRisingEdge"
            else:
                fn = "_onFallingEdge"
            op0 = self.as_hdl_Value(ops[0])
            # pop .val
            op0 = op0.ops[0]
            return hdl_call(hdl_getattr(op0, fn), [])
        elif o in [AllOps.BitsAsUnsigned, AllOps.BitsAsVec, AllOps.BitsAsSigned]:
            op0, = ops
            do_cast = bool(op0._dtype.signed) != bool(op.result._dtype.signed)

            op_hdl = self.as_hdl_Value(op0)
            if do_cast:
                if bool(op0._dtype.signed):
                    sign = self.TRUE
                else:
                    sign = self.FALSE
                    # cast_sign()
                return hdl_call(hdl_getattr(op_hdl, "cast_sign"), [sign, ])
            else:
                return op_hdl
        elif o == AllOps.CONCAT:
            return hdl_call(hdl_getattr(self.as_hdl_Value(ops[0]), "_concat"),
                            [self.as_hdl_Value(ops[1]), ])
        elif o == AllOps.EQ:
            return hdl_call(hdl_getattr(self.as_hdl_Value(ops[0]), "_eq"),
                            [self.as_hdl_Value(ops[1]), ])
        else:
            o = self.op_transl_dict[o]
            return HdlOp(o, [self.as_hdl_Value(o2)
                               for o2 in ops])
