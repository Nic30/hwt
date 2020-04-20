from hdlConvertor.hdlAst._expr import HdlCall, HdlBuiltinFn, HdlName
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.bits import Bits


class ToHdlAstSystemC_type():

    def HdlType_bits(self, typ, declaration=False):
        if declaration:
            raise NotImplementedError()

        w = typ.bit_length()

        if w <= 64:
            if typ.signed:
                typeBaseName = "int"
            else:
                typeBaseName = "uint"
        else:
            if typ.signed:
                typeBaseName = "bigint"
            else:
                typeBaseName = "biguint"

        return HdlCall(HdlBuiltinFn.PARAMETRIZATION, [HdlName("sc_%s" % typeBaseName, obj=LanguageKeyword()),
                                                      self.as_hdl_int(w)])

    def HdlType_enum(self, typ, declaration=False):
        if declaration:
            raise TypeError(
                "There is problem with tracing of c enums, use Bits instead")
        else:
            valueCnt = len(typ._allValues)
            return self.as_hdl_HdlType_bits(Bits(valueCnt.bit_length()),
                                            declaration=declaration)
