from hdlConvertorAst.hdlAst import HdlValueId, HdlValueInt
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call,\
    hdl_getattr
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.slice import Slice
from pyMathBitPrecise.bits3t import Bits3t


class ToHdlAstSimModel_types():
    """
    part of ToHdlAstSimModel responsible for type serialization
    """
    SELF = HdlValueId("self", obj=LanguageKeyword())
    BITS3T = HdlValueId("Bits3t", obj=Bits3t)
    SLICE = HdlValueId("slice", obj=slice)

    def as_hdl_HdlType_bits(self, typ: Bits, declaration=False):
        assert not declaration
        w = typ.bit_length()
        if isinstance(w, int):
            pass
        else:
            w = int(w)

        return hdl_call(self.BITS3T, [HdlValueInt(w, None, None),
                                      HdlValueInt(int(bool(typ.signed)), None, None)])

    def as_hdl_HdlType_slice(self, typ: Slice, declaration=False):
        if declaration:
            raise NotImplementedError()
        else:
            return self.SLICE

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
