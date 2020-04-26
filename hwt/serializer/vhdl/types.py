from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.typeCast import toHVal
from hdlConvertor.hdlAst._expr import HdlName, HdlCall, HdlBuiltinFn,\
    HdlTypeType
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.hdl.types.defs import BOOL, INT
from hdlConvertor.hdlAst._defs import HdlVariableDef
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_index,\
    hdl_downto
from hwt.hdl.types.array import HArray


class ToHdlAstVhdl2008_types():
    BOOLEAN = HdlName("BOOLEAN", obj=LanguageKeyword())
    INTEGER = HdlName("INTEGER", obj=LanguageKeyword())
    STRING = HdlName("STRING", obj=LanguageKeyword())
    STD_LOGIC_VECTOR = HdlName("STD_LOGIC_VECTOR", obj=LanguageKeyword())
    STD_LOGIC = HdlName("STD_LOGIC", obj=LanguageKeyword())
    SIGNED = HdlName("SIGNED", obj=LanguageKeyword())
    UNSIGNED = HdlName("UNSIGNED", obj=LanguageKeyword())

    def as_hdl_HdlType(self, typ: HdlType, declaration=False):
        """
        Serialize HdlType instance
        """
        try:
            to_vhdl = typ._to_vhdl
        except AttributeError:
            to_vhdl = None
            pass
        if to_vhdl is not None:
            return to_vhdl(self, typ, declaration=declaration)
        else:
            return super(ToHdlAstVhdl2008_types, self).as_hdl_HdlType(typ, declaration)

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

        return HdlCall(HdlBuiltinFn.CALL, [
            name,
            HdlCall(HdlBuiltinFn.DOWNTO, [
                self.as_hdl_int(w - 1),
                self.as_hdl_int(0)
            ])])

    def as_hdl_HdlType_array(self, typ: HArray, declaration=False):
        if declaration:
            v = HdlVariableDef()
            name = getattr(typ, "name", None)
            if name is None:
                name = "arr_t_"
            typ.name = v.name = self.name_scope.checkedName(name, typ)
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

