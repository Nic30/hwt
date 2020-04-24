from hdlConvertor.hdlAst._expr import HdlCall, HdlBuiltinFn, HdlName
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum


class ToHdlAstSystemC_type():
    sc_int = HdlName("sc_int", obj=LanguageKeyword())
    sc_uint = HdlName("sc_uint", obj=LanguageKeyword())
    sc_bigint = HdlName("sc_bigint", obj=LanguageKeyword())
    sc_biguint = HdlName("sc_biguint", obj=LanguageKeyword())

    def as_hdl_HdlType_bits(self, typ: Bits, declaration=False):
        if declaration:
            raise NotImplementedError()

        w = typ.bit_length()

        if w <= 64:
            if typ.signed:
                typeBaseName = self.sc_int
            else:
                typeBaseName = self.sc_uint
        else:
            if typ.signed:
                typeBaseName = self.sc_bigint
            else:
                typeBaseName = self.sc_biguint

        return HdlCall(HdlBuiltinFn.PARAMETRIZATION,
                       [typeBaseName, self.as_hdl_int(w)])

    def as_hdl_HdlType_enum(self, typ: HEnum, declaration=False):
        if declaration:
            raise TypeError(
                "There is problem with tracing of c enums, use Bits instead")
        else:
            valueCnt = len(typ._allValues)
            return self.as_hdl_HdlType_bits(Bits(valueCnt.bit_length()),
                                            declaration=declaration)
