from hdlConvertor.hdlAst import HdlVariableDef,  HdlName, HdlIntValue,\
    HdlTypeType, HdlEnumDef
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call,\
    hdl_getattr
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.bits import Bits
from pyMathBitPrecise.bits3t import Bits3t


class ToHdlAstSimModel_types():
    """
    part of ToHdlAstSimModel responsible for type serialization
    """
    SELF = HdlName("self", obj=LanguageKeyword())
    BITS3T = HdlName("Bits3t", obj=Bits3t)

    def as_hdl_HdlType_bits(self, typ: Bits, declaration=False):
        assert not declaration
        w = typ.bit_length()
        if isinstance(w, int):
            pass
        else:
            w = int(w)

        return hdl_call(self.BITS3T, [HdlIntValue(w, None, None),
                                      HdlIntValue(int(bool(typ.signed)), None, None)])

    def as_hdl_HdlType_array(self, typ, declaration=False):
        if declaration:
            return super(ToHdlAstSimModel_types, self).as_hdl_HdlType_array(typ, declaration=declaration)
        else:
            t_name = self.name_scope.get_object_name(typ)
            return hdl_getattr(self.SELF, t_name)

    def as_hdl_HdlType_enum(self, typ, declaration=False):
        if declaration:
            return super(ToHdlAstSimModel_types, self).as_hdl_HdlType_enum(typ, declaration=True)
        else:
            t_name = self.name_scope.get_object_name(typ)
            return hdl_getattr(self.SELF, t_name)
