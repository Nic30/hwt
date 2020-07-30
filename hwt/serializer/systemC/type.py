from hdlConvertorAst.hdlAst._expr import HdlOp, HdlOpType, HdlValueId
from hdlConvertorAst.to.verilog.constants import SIGNAL_TYPE
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.hdlType import MethodNotOverloaded
from hwt.serializer.verilog.types import ToHdlAstVerilog_types


class ToHdlAstSystemC_type():
    sc_int = HdlValueId("sc_int", obj=LanguageKeyword())
    sc_uint = HdlValueId("sc_uint", obj=LanguageKeyword())
    sc_bigint = HdlValueId("sc_bigint", obj=LanguageKeyword())
    sc_biguint = HdlValueId("sc_biguint", obj=LanguageKeyword())
    sc_signal = HdlValueId("sc_signal", obj=LanguageKeyword())
    STRING = HdlOp(HdlOpType.DOUBLE_COLON, HdlValueId("string", obj=LanguageKeyword()))

    def does_type_requires_extra_def(self, t, other_types):
        try:
            return t._as_hdl_requires_def(self, other_types)
        except MethodNotOverloaded:
            pass
        return False

    def as_hdl_HdlType_str(self, typ, declaration=False):
        assert not declaration
        return self.STRING

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

        t = HdlOp(HdlOpType.PARAMETRIZATION,
                    [typeBaseName, self.as_hdl_int(w)])
        if self.signalType == SIGNAL_TYPE.WIRE:
            t = HdlOp(HdlOpType.PARAMETRIZATION, [self.sc_signal, t])
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
