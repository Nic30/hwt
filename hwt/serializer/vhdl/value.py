from hdlConvertorAst.hdlAst import HdlValueId, HdlValueInt, HdlOp, \
    HdlOpType
from hdlConvertorAst.to.hdlUtils import bit_string
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsConst import HBitsConst
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.enumConst import HEnumConst
from hwt.hdl.types.sliceConst import HSliceConst
from hwt.mainBases import RtlSignalBase
from hwt.serializer.generic.value import ToHdlAst_Value


class ToHdlAstVhdl2008_Value(ToHdlAst_Value):

    TRUE = HdlValueId("TRUE", obj=LanguageKeyword())
    FALSE = HdlValueId("FALSE", obj=LanguageKeyword())
    # TO_UNSIGNED = HdlValueId("TO_UNSIGNED", obj=LanguageKeyword())
    # TO_SIGNED = HdlValueId("TO_SIGNED", obj=LanguageKeyword())

    def as_hdl_cond(self, c, forceBool):
        assert isinstance(c, (RtlSignalBase, HConst)), c
        if not forceBool or c._dtype == BOOL:
            return self.as_hdl(c)
        elif c._dtype == BIT:
            return self.as_hdl(c._eq(1))
        elif isinstance(c._dtype, HBits):
            return self.as_hdl(c != 0)
        else:
            raise NotImplementedError()

    def as_hdl_HEnumConst(self, val: HEnumConst):
        name = self.name_scope.get_object_name(val)
        return HdlValueId(name, obj=val)

    def as_hdl_HArrayConst(self, val):
        return [self.as_hdl_Value(v) for v in val]

    def sensitivityListItem(self, item, anyIsEventDependnt):
        if isinstance(item, HOperatorNode):
            item = item.operands[0]
        return self.as_hdl(item)

    def as_hdl_BitString(self, v, width: int,
                         force_vector: bool, vld_mask: int, signed):
        is_bit = not force_vector and width == 1
        # if vld_mask != mask(width) or width >= 32 or is_bit:
        v = bit_string(v, width, vld_mask)
        if is_bit:
            v.base = 256
            return v
        if signed is None:
            return v
        elif signed:
            cast = self.SIGNED
        else:
            cast = self.UNSIGNED
        return HdlOp(HdlOpType.APOSTROPHE, [cast, v])

        # else:
        #    v = HdlValueInt(v, None, None)
        #
        #    if signed is None:
        #        return v
        #    elif signed:
        #        cast_fn = self.TO_SIGNED
        #    else:
        #        cast_fn = self.TO_UNSIGNED
        #    return hdl_call(cast_fn, [v, HdlValueInt(width, None, None)])

    def as_hdl_HBoolConst(self, val: HBitsConst):
        if val.val:
            return self.TRUE
        else:
            return self.FALSE

    def as_hdl_HBitsConst(self, val: HBitsConst):
        t = val._dtype
        v = super(ToHdlAstVhdl2008_Value, self).as_hdl_HBitsConst(val)
        # handle '1' vs "1" difference (bit literal vs vector)
        if not t.force_vector and t.bit_length() == 1 and t != BOOL:
            if isinstance(v, HdlValueInt):
                v.base = 256
            else:
                # assert is cast
                assert isinstance(v, HdlOp) and v.fn == HdlOpType.CALL, v
                _v = v.ops[1]
                if isinstance(_v, HdlValueInt):
                    _v.base = 256
                else:
                    raise NotImplementedError()
        return v

    def as_hdl_HSliceConst(self, val: HSliceConst):
        upper = val.val.start
        if int(val.val.step) == -1:
            if isinstance(upper, HConst):
                upper = HdlValueInt(int(upper) - 1, None, None)
            else:
                upper = HdlOp(HdlOpType.SUB, [self.as_hdl_Value(upper),
                                                   HdlValueInt(1, None, None)])
        else:
            raise NotImplementedError(val.val.step)

        return HdlOp(HdlOpType.DOWNTO, [upper, self.as_hdl(val.val.stop)])
