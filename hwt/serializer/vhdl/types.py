from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOp, HdlOpType,\
    HdlTypeType
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index,\
    hdl_downto
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, INT


class ToHdlAstVhdl2008_types():
    BOOLEAN = HdlValueId("BOOLEAN", obj=LanguageKeyword())
    INTEGER = HdlValueId("INTEGER", obj=LanguageKeyword())
    STRING = HdlValueId("STRING", obj=LanguageKeyword())
    STD_LOGIC_VECTOR = HdlValueId("STD_LOGIC_VECTOR", obj=LanguageKeyword())
    STD_LOGIC = HdlValueId("STD_LOGIC", obj=LanguageKeyword())
    SIGNED = HdlValueId("SIGNED", obj=LanguageKeyword())
    UNSIGNED = HdlValueId("UNSIGNED", obj=LanguageKeyword())

    def as_hdl_HdlType_str(self, typ, declaration=False):
        assert not declaration
        return self.STRING

    def as_hdl_HdlType_bits(self, typ: Bits, declaration=False):
        if declaration:
            raise NotImplementedError()
        if typ == BOOL:
            return self.BOOLEAN
        if typ == INT:
            return self.INTEGER

        bitLength = typ.bit_length()
        w = typ.bit_length()
        isVector = typ.force_vector or bitLength > 1

        if typ.signed is None:
            if isVector:
                name = self.STD_LOGIC_VECTOR
            else:
                return self.STD_LOGIC
        elif typ.signed:
            name = self.SIGNED
        else:
            name = self.UNSIGNED

        return HdlOp(HdlOpType.CALL, [
            name,
            HdlOp(HdlOpType.DOWNTO, [
                self.as_hdl(w - 1),
                self.as_hdl_int(0)
            ])])

    def as_hdl_HdlType_array(self, typ: HArray, declaration=False):
        if declaration:
            v = HdlIdDef()
            name = getattr(typ, "name", None)
            if name is None:
                name = "arr_t_"
            v.name = self.name_scope.checked_name(name, typ)
            v.type = HdlTypeType
            v.origin = typ
            size = hdl_downto(
                self.as_hdl_int(int(typ.size) - 1),
                self.as_hdl_int(0)
            )
            if self.does_type_requires_extra_def(typ.element_t, ()):
                raise NotImplementedError(typ.element_t)
            e_t = self.as_hdl_HdlType(typ.element_t, declaration=False)
            v.value = hdl_index(e_t, size)
            return v
        else:
            return super(ToHdlAstVhdl2008_types, self).as_hdl_HdlType_array(typ, declaration)
