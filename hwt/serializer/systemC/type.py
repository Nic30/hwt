from hdlConvertor.hdlAst._expr import HdlCall, HdlBuiltinFn, HdlName
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.serializer.verilog.types import ToHdlAstVerilog_types
from hdlConvertor.to.verilog.constants import SIGNAL_TYPE


class ToHdlAstSystemC_type():
    sc_int = HdlName("sc_int", obj=LanguageKeyword())
    sc_uint = HdlName("sc_uint", obj=LanguageKeyword())
    sc_bigint = HdlName("sc_bigint", obj=LanguageKeyword())
    sc_biguint = HdlName("sc_biguint", obj=LanguageKeyword())
    sc_signal = HdlName("sc_signal", obj=LanguageKeyword())

    def does_type_requires_extra_def(self, t, other_types):
        return False

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

        t = HdlCall(HdlBuiltinFn.PARAMETRIZATION,
                    [typeBaseName, self.as_hdl_int(w)])
        if self.signalType == SIGNAL_TYPE.WIRE:
            t = HdlCall(HdlBuiltinFn.PARAMETRIZATION, [self.sc_signal, t])
        return t

    def as_hdl_HdlType_array(self, typ: HArray, declaration=False):
        if declaration:
            return super(ToHdlAstSystemC_type, self).as_hdl_HdlType_array(
                self, typ, declaration=declaration)
        else:
            _int = self.as_hdl_int
            size = _int(int(typ.size))
            return hdl_index(self.as_hdl_HdlType(typ.element_t), size)

    def as_hdl_HdlType_enum(self, typ: HEnum, declaration=False):
        return ToHdlAstVerilog_types.as_hdl_HdlType_enum(
            self, typ, declaration=declaration)
