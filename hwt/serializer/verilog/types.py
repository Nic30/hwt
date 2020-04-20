from hdlConvertor.hdlAst._expr import HdlTypeAuto, HdlName, HdlCall,\
    HdlBuiltinFn
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index,\
    hdl_downto
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT
from hwt.serializer.verilog.utils import SIGNAL_TYPE


class ToHdlAstVerilog_types():
    NULL = HdlName("null")

    def does_type_requires_extra_def(self, t, other_types):
        return False

    def as_hdl_HdlType_bits(self, typ: Bits, declaration=False):
        isVector = typ.force_vector or typ.bit_length() > 1
        sigType = self.signalType

        if typ == INT:
            t = HdlName("int", obj=int)
        elif sigType is SIGNAL_TYPE.PORT_WIRE:
            t = HdlTypeAuto
        elif sigType is SIGNAL_TYPE.REG or sigType is SIGNAL_TYPE.PORT_REG:
            t = HdlName("reg", obj=LanguageKeyword())
        elif sigType is SIGNAL_TYPE.WIRE:
            t = HdlName("wire", obj=LanguageKeyword())
        else:
            raise ValueError(sigType)

        if typ.signed is None:
            is_signed = self.NULL
        else:
            is_signed = self.as_hdl_int(int(typ.signed))

        if isVector:
            w = typ.bit_length()
            assert isinstance(w, int), w
            w = hdl_downto(self.as_hdl_int(w - 1),
                           self.as_hdl_int(0))
        else:
            w = self.NULL

        return HdlCall(HdlBuiltinFn.PARAMETRIZATION, [t, w, is_signed])

    def as_hdl_HdlType_array(self, typ: HArray, declaration=False):
        if declaration:
            return super(ToHdlAstVerilog_types, self).as_hdl_HdlType_array()
        else:
            _int = self.as_hdl_int
            size = HdlCall(HdlBuiltinFn.DOWNTO, [_int(0),
                                                 _int(int(typ.size))])
            return hdl_index(self.as_hdl_HdlType(typ.element_t), size)

    def as_hdl_HdlType_enum(self, typ, declaration=False):
        if declaration:
            raise TypeError(
                "Verilog does not have enum types, hwt uses Bits instead"
                " (this should not be required because it should have been filtered before)")
        else:
            valueCnt = len(typ._allValues)
            return self.as_hdl_HdlType_bits(Bits(valueCnt.bit_length()),
                                            declaration=declaration)
