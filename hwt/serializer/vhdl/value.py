from hdlConvertor.hdlAst import HdlName, HdlIntValue, HdlCall,\
    HdlBuiltinFn
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.hdl.operator import Operator
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.defs import BOOL, BIT
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.value import Value
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyMathBitPrecise.bit_utils import mask
from hdlConvertor.to.hdlUtils import bit_string


class ToHdlAstVhdl2008_Value(ToHdlAst_Value):

    TRUE = HdlName("TRUE", obj=LanguageKeyword())
    FALSE = HdlName("FALSE", obj=LanguageKeyword())
    TO_UNSIGNED = HdlName("TO_UNSIGNED", obj=LanguageKeyword())
    TO_SIGNED = HdlName("TO_SIGNED", obj=LanguageKeyword())

    def as_hdl_cond(self, c, forceBool):
        assert isinstance(c, (RtlSignalBase, Value)), c
        if not forceBool or c._dtype == BOOL:
            return self.as_hdl(c)
        elif c._dtype == BIT:
            return self.as_hdl(c._eq(1))
        elif isinstance(c._dtype, Bits):
            return self.as_hdl(c != 0)
        else:
            raise NotImplementedError()

    def as_hdl_HEnumVal(self, val: HEnumVal):
        return HdlName(val.val, obj=val)

    def as_hdl_HArrayVal(self, val):
        return [self.as_hdl_Value(v) for v in val]

    def sensitivityListItem(self, item, anyIsEventDependnt):
        if isinstance(item, Operator):
            item = item.operands[0]
        return self.as_hdl(item)

    def as_hdl_BitString(self, v, width: int,
                         force_vector: bool, vld_mask: int, signed):

        if vld_mask != mask(width):
            v = bit_string(v, width, vld_mask)
            if not force_vector and width == 1:
                v.base = 256
        else:
            v = bit_string(v, width, vld_mask)

        if signed is None:
            return v
        elif signed:
            cast_fn = self.TO_SIGNED
        else:
            cast_fn = self.TO_UNSIGNED

        # [TODO] parametrized width
        return hdl_call(cast_fn, [v, HdlIntValue(width, None, None)])

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
            if isinstance(v, HdlIntValue):
                v.base = 256
            else:
                # assert is cast
                assert isinstance(v, HdlCall) and v.fn == HdlBuiltinFn.CALL, v
                _v = v.ops[1]
                if isinstance(_v, HdlIntValue):
                    _v.base = 256
                else:
                    raise NotImplementedError()
        return v

    def as_hdl_SliceVal(self, val: SliceVal):
        upper = val.val.start
        if int(val.val.step) == -1:
            if isinstance(upper, Value):
                upper = HdlIntValue(int(upper) - 1, None, None)
            else:
                upper = HdlCall(HdlBuiltinFn.SUB, [self.as_hdl_Value(upper),
                                                   HdlIntValue(1, None, None)])
        else:
            raise NotImplementedError(val.val.step)

        return HdlCall(HdlBuiltinFn.DOWNTO, [upper, self.as_hdl(val.val.stop)])
