from typing import Union

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOp, HdlOpType
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call, \
    hdl_getattr
from hwt.code import Concat
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsConst import HBitsConst
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumConst import HEnumConst
from hwt.hdl.variables import HdlSignalItem
from hwt.pyUtils.typingFuture import override
from hwt.serializer.generic.ops import HWT_TO_HDLCONVERTOR_OPS
from hwt.serializer.generic.value import ToHdlAst_Value
from pyMathBitPrecise.array3t import Array3val
from pyMathBitPrecise.bits3t import Bits3val, Bits3t, bitsBitOp__lshr, \
    bitsBitOp__rol, bitsBitOp__ror

zero, one = BIT.from_py(0), BIT.from_py(1)


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
    FN_bitsBitOp__lshr = HdlValueId("bitsBitOp__lshr", obj=bitsBitOp__lshr)
    FN_bitsBitOp__rol = HdlValueId("bitsBitOp__rol", obj=bitsBitOp__rol)
    FN_bitsBitOp__ror = HdlValueId("bitsBitOp__ror", obj=bitsBitOp__ror)

    op_transl_dict = {
        **HWT_TO_HDLCONVERTOR_OPS,
        HwtOps.INDEX: HdlOpType.INDEX,
    }
    _cast_ops = {
        HwtOps.BitsAsSigned,
        HwtOps.BitsAsUnsigned,
        HwtOps.BitsAsVec,
    }

    def is_suitable_for_const_extract(self, val: HConst):
        return not isinstance(val._dtype, HEnum) or val.vld_mask == 0

    @override
    def as_hdl_HdlSignalItem(self, si: Union[HdlSignalItem, HdlIdDef],
                          declaration=False):
        if not declaration and not si._isUnnamedExpr:
            if si._const:
                return hdl_getattr(self.SELF, si._name)
            else:
                return hdl_getattr(hdl_getattr(self.SELF_IO, si._name), "val")
        else:
            return super(ToHdlAstSimModel_value, self).as_hdl_HdlSignalItem(
                si, declaration=declaration)

    @override
    def as_hdl_HBitsConst(self, val: HBitsConst):
        dtype = val._dtype
        as_hdl_int = self.as_hdl_int
        t = hdl_call(self.Bits3t, [
            as_hdl_int(dtype.bit_length()), as_hdl_int(int(bool(dtype.signed)))])
        return hdl_call(self.Bits3val, [t,
                                        as_hdl_int(val.val),
                                        as_hdl_int(val.vld_mask)])

    def as_hdl_HDictConst(self, val):
        return {
            self.as_hdl_int(int(k)): self.as_hdl_Value(v)
            for k, v in val.items()
        }

    @override
    def as_hdl_HArrayConst(self, val):
        return hdl_call(self.Array3val, [
            self.as_hdl_HdlType(val._dtype),
            self.as_hdl_HDictConst(val.val),
            self.as_hdl_int(val.vld_mask)
        ])

    @override
    def as_hdl_HSliceConst(self, val):
        args = (
            val.val.start,
            val.val.stop,
            val.val.step
        )
        return hdl_call(self.SLICE, [self.as_hdl_int(int(a)) for a in args])

    @override
    def as_hdl_HEnumConst(self, val: HEnumConst):
        t_name = self.name_scope.get_object_name(val._dtype)
        if val.vld_mask:
            name = self.name_scope.get_object_name(val)
            return hdl_getattr(hdl_getattr(self.SELF, t_name), name)
        else:
            return hdl_call(hdl_getattr(hdl_getattr(self.SELF, t_name), "from_py"),
                            [None, ])

    @override
    def as_hdl_HOperatorNode(self, op: HOperatorNode):
        ops = op.operands
        o = op.operator

        if o == HwtOps.EQ:
            op0 = self.as_hdl_Value(ops[0])
            op1 = self.as_hdl_Value(ops[1])
            return hdl_call(hdl_getattr(op0, "_eq"), [op1, ])
        elif o == HwtOps.TERNARY:
            if ops[1] == one and ops[2] == zero:
                # ignore redundant x ? 1 : 0
                return self.as_hdl_cond(ops[0], True)
            else:
                op0 = self.as_hdl_cond(ops[0], True)
                op1 = self.as_hdl_Value(ops[1])
                op2 = self.as_hdl_Value(ops[2])
                return hdl_call(hdl_getattr(op0, "_ternary"), [op1, op2])
        elif o == HwtOps.RISING_EDGE or o == HwtOps.FALLING_EDGE:
            if o == HwtOps.RISING_EDGE:
                fn = "_onRisingEdge"
            else:
                fn = "_onFallingEdge"
            op0 = self.as_hdl_Value(ops[0])
            # pop .val
            op0 = op0.ops[0]
            return hdl_call(hdl_getattr(op0, fn), [])
        elif o in self._cast_ops:
            op0, = ops
            do_cast = bool(op0._dtype.signed) != bool(op.result._dtype.signed)

            op_hdl = self.as_hdl_Value(op0)
            if do_cast:
                if bool(op.result._dtype.signed):
                    sign = self.TRUE
                else:
                    sign = self.FALSE
                return hdl_call(hdl_getattr(op_hdl, "cast_sign"), [sign, ])
            else:
                return op_hdl
        elif o == HwtOps.CONCAT:
            return hdl_call(hdl_getattr(self.as_hdl_Value(ops[0]), "_concat"),
                            [self.as_hdl_Value(ops[1]), ])
        elif o == HwtOps.EQ:
            return hdl_call(hdl_getattr(self.as_hdl_Value(ops[0]), "_eq"),
                            [self.as_hdl_Value(ops[1]), ])
        else:
            _o = o.hdlConvertoAstOp
            if _o is None:
                try:
                    o = self.op_transl_dict[o]
                except:
                    raise
            else:
                o = _o

            if o == HdlOpType.SRL and isinstance(ops[0]._dtype, HBits) and ops[0]._dtype.signed:
                return hdl_call(self.FN_bitsBitOp__lshr,
                            [self.as_hdl_Value(o2)
                               for o2 in ops])
            elif o == HdlOpType.ROL and isinstance(ops[0]._dtype, HBits):
                return hdl_call(self.FN_bitsBitOp__rol,
                            [self.as_hdl_Value(o2) for o2 in ops])
            elif o == HdlOpType.ROR and isinstance(ops[0]._dtype, HBits):
                return hdl_call(self.FN_bitsBitOp__ror,
                            [self.as_hdl_Value(o2) for o2 in ops])

            return HdlOp(o, [self.as_hdl_Value(o2)
                               for o2 in ops])
