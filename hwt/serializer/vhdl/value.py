from hdlConvertorAst.hdlAst import HdlValueId, HdlValueInt, HdlOp,\
    HdlOpType
from hdlConvertorAst.to.hdlUtils import bit_string
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.hdl.operator import Operator
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.value import HValue
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class ToHdlAstVhdl2008_Value(ToHdlAst_Value):

    TRUE = HdlValueId("TRUE", obj=LanguageKeyword())
    FALSE = HdlValueId("FALSE", obj=LanguageKeyword())
    #TO_UNSIGNED = HdlValueId("TO_UNSIGNED", obj=LanguageKeyword())
    #TO_SIGNED = HdlValueId("TO_SIGNED", obj=LanguageKeyword())

    def as_hdl_cond(self, c, forceBool):
        assert isinstance(c, (RtlSignalBase, HValue)), c
        if not forceBool or c._dtype == BOOL:
            return self.as_hdl(c)
        elif c._dtype == BIT:
            return self.as_hdl(c._eq(1))
        elif isinstance(c._dtype, Bits):
            return self.as_hdl(c != 0)
        else:
            raise NotImplementedError()

    def as_hdl_HEnumVal(self, val: HEnumVal):
        name = self.name_scope.get_object_name(val)
        return HdlValueId(name, obj=val)

    def as_hdl_HArrayVal(self, val):
        return [self.as_hdl_Value(v) for v in val]

    def sensitivityListItem(self, item, anyIsEventDependnt):
        if isinstance(item, Operator):
            item = item.operands[0]
        return self.as_hdl(item)

    def as_hdl_BitString(self, v, width: int,
                         force_vector: bool, vld_mask: int, signed):
        is_bit = not force_vector and width == 1
        #if vld_mask != mask(width) or width >= 32 or is_bit:
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

        #else:
        #    v = HdlValueInt(v, None, None)
        #
        #    if signed is None:
        #        return v
        #    elif signed:
        #        cast_fn = self.TO_SIGNED
        #    else:
        #        cast_fn = self.TO_UNSIGNED
        #    return hdl_call(cast_fn, [v, HdlValueInt(width, None, None)])

    def as_hdl_BoolVal(self, val: BitsVal):
        if val.val:
            return self.TRUE
        else:
            return self.FALSE

    def as_hdl_BitsVal(self, val: BitsVal):
        t = val._dtype
        v = super(ToHdlAstVhdl2008_Value, self).as_hdl_BitsVal(val)
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

    def as_hdl_SliceVal(self, val: SliceVal):
        upper = val.val.start
        if int(val.val.step) == -1:
            if isinstance(upper, HValue):
                upper = HdlValueInt(int(upper) - 1, None, None)
            else:
                upper = HdlOp(HdlOpType.SUB, [self.as_hdl_Value(upper),
                                                   HdlValueInt(1, None, None)])
        else:
            raise NotImplementedError(val.val.step)

        return HdlOp(HdlOpType.DOWNTO, [upper, self.as_hdl(val.val.stop)])
