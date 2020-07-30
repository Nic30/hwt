from hdlConvertorAst.hdlAst._expr import HdlTypeAuto, HdlValueId, HdlOp,\
    HdlOpType
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index,\
    hdl_downto
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT
from hwt.hdl.types.hdlType import HdlType, MethodNotOverloaded
from hwt.serializer.verilog.utils import SIGNAL_TYPE


class ToHdlAstVerilog_types():

    def does_type_requires_extra_def(self, t: HdlType, other_types: list):
        try:
            return t._as_hdl_requires_def(self, other_types)
        except MethodNotOverloaded:
            pass
        return False

    def as_hdl_HdlType_bits(self, typ: Bits, declaration=False):
        isVector = typ.force_vector or typ.bit_length() > 1
        sigType = self.signalType

        if typ == INT:
            t = HdlValueId("int", obj=int)
        elif sigType is SIGNAL_TYPE.PORT_WIRE:
            t = HdlTypeAuto
        elif sigType is SIGNAL_TYPE.REG or sigType is SIGNAL_TYPE.PORT_REG:
            t = HdlValueId("reg", obj=LanguageKeyword())
        elif sigType is SIGNAL_TYPE.WIRE:
            t = HdlValueId("wire", obj=LanguageKeyword())
        else:
            raise ValueError(sigType)

        if typ.signed is None:
            is_signed = None
        else:
            is_signed = self.as_hdl_int(int(typ.signed))

        if isVector:
            w = typ.bit_length()
            assert isinstance(w, int), w
            w = hdl_downto(self.as_hdl_int(w - 1),
                           self.as_hdl_int(0))
        else:
            w = None

        return HdlOp(HdlOpType.PARAMETRIZATION, [t, w, is_signed])

    def as_hdl_HdlType_array(self, typ: HArray, declaration=False):
        if declaration:
            raise NotImplementedError()
        else:
            _int = self.as_hdl_int
            size = HdlOp(HdlOpType.DOWNTO, [_int(0),
                                                 _int(int(typ.size) - 1)])
            return hdl_index(self.as_hdl_HdlType(typ.element_t), size)

    def as_hdl_HdlType_enum(self, typ, declaration=False):
        if declaration:
            raise TypeError(
                "Target language does not use enum types, this library should uses Bits instead"
                " (this should not be required because it should have been filtered before)")
        else:
            valueCnt = len(typ._allValues)
            return self.as_hdl_HdlType_bits(Bits(valueCnt.bit_length()),
                                            declaration=declaration)
