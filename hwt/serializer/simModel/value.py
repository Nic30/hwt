from typing import Union

from hdlConvertor.hdlAst._defs import HdlVariableDef
from hdlConvertor.hdlAst._expr import HdlName, HdlCall, HdlBuiltinFn
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call,\
    hdl_getattr
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.enum import HEnum
from hwt.hdl.variables import SignalItem
from hwt.serializer.generic.value import ToHdlAst_Value
from pyMathBitPrecise.array3t import Array3val
from pyMathBitPrecise.bits3t import Bits3val, Bits3t
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BIT
from hwt.serializer.generic.ops import HWT_TO_HDLCONVEROTR_OPS
from hwt.code import Concat


class ToHdlAstSimModel_value(ToHdlAst_Value):
    Bits3val = HdlName("Bits3val", obj=Bits3val)
    Bits3t = HdlName("Bits3t", obj=Bits3t)
    SELF = HdlName("self", obj=LanguageKeyword())
    Array3val = HdlName("Array3val", obj=Array3val)
    SLICE = HdlName("slice", obj=slice)
    TRUE = HdlName("True", obj=True)
    FALSE = HdlName("False", obj=False)
    Bits3val = HdlName("Bits3val", obj=Bits3val)
    ABits3t = HdlName("Bits3t", obj=Bits3t)
    SELF_IO = hdl_getattr(HdlName("self", obj=LanguageKeyword()), "io")
    CONCAT = HdlName("Concat", obj=Concat)
    op_transl_dict = {
        **HWT_TO_HDLCONVEROTR_OPS,
        AllOps.INDEX: HdlBuiltinFn.INDEX,
    }

    def as_hdl_SignalItem(self, si: Union[SignalItem, HdlVariableDef],
                          declaration=False):
        if not declaration and not si.hidden:
            return hdl_getattr(hdl_getattr(self.SELF_IO, si.name), "val")
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

    def Value_try_extract_as_const(self, val):
        return None
        # raise NotImplementedError()
        # try to extract value as constant
        try:
            consGetter = self.constCache.getConstName
        except AttributeError:
            consGetter = None

        if consGetter and not isinstance(val._dtype, HEnum):
            return hdl_getattr(self.SELF, consGetter(val))

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

    def as_hdl_HEnumVal(self, val):
        return hdl_getattr(hdl_getattr(self.SELF,val._dtype.name), val.val)

    def as_hdl_Operator(self, op: Operator):
        ops = op.operands
        o = op.operator

        if o == AllOps.EQ:
            op0 = self.as_hdl(ops[0])
            op1 = self.as_hdl(ops[1])
            return hdl_call(hdl_getattr(op0, "_eq"), [op1, ])
        elif o == AllOps.TERNARY:
            zero, one = BIT.from_py(0), BIT.from_py(1)
            if ops[1] == one and ops[2] == zero:
                # ignore redundant x ? 1 : 0
                return self.as_hdl_cond([ops[0]], True)
            else:
                op0 = self.as_hdl_cond([ops[0]], True)
                op1 = self.as_hdl(ops[1], op)
                op2 = self.as_hdl(ops[2], op)
                return hdl_call(hdl_getattr(op0, "_ternary"), [op1, op2])
        elif o == AllOps.RISING_EDGE or o == AllOps.FALLING_EDGE:
            if o == AllOps.RISING_EDGE:
                fn = "_onRisingEdge"
            else:
                fn = "_onFallingEdge"
            op0 = self.as_hdl(ops[0])
            # pop .val
            op0 = op0.ops[0]
            return hdl_call(hdl_getattr(op0, fn), [])
        elif o in [AllOps.BitsAsUnsigned, AllOps.BitsAsVec, AllOps.BitsAsSigned]:
            op0, = ops
            do_cast = bool(op0._dtype.signed) != bool(op.result._dtype.signed)

            op_hdl = self.as_hdl(op0)
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
            return hdl_call(hdl_getattr(self.as_hdl(ops[0]), "_concat"),
                            [self.as_hdl(ops[1]), ])
        elif o == AllOps.EQ:
            return hdl_call(hdl_getattr(self.as_hdl(ops[0]), "_eq"),
                            [self.as_hdl(ops[1]), ])
        else:
            o = self.op_transl_dict[o]
            return HdlCall(o, [self.as_hdl(o2)
                               for o2 in ops])
