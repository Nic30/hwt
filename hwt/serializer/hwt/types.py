from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlValueInt
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call,\
    hdl_map_asoc, hdl_index
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import BITS_DEFAUTL_SIGNED, BITS_DEFAUTL_FORCEVECTOR, \
    BITS_DEFAUTL_NEGATED, Bits
from hwt.hdl.types.defs import BOOL, INT
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.hdlType import MethodNotOverloaded


class ToHdlAstHwt_types():
    """
    part of ToHdlAstSimModel responsible for type serialization
    """
    BOOL = HdlValueId("BOOL", obj=BOOL)
    INT = HdlValueId("INT", obj=INT)
    BITS = HdlValueId("Bits", obj=Bits)

    def does_type_requires_extra_def(self, t, other_types):
        try:
            return t._as_hdl_requires_def(self, other_types)
        except MethodNotOverloaded:
            pass
        return isinstance(t, HEnum) and t not in other_types

    def as_hdl_HdlType_array(self, typ: HArray, declaration=False):
        assert not declaration, "declaration should not be required"
        t = self.as_hdl_HdlType(typ.element_t, declaration=declaration)
        return hdl_index(t, HdlValueInt(int(typ.size), None, None))

    def as_hdl_HdlType_bits(self, typ: Bits, declaration=False):
        if declaration:
            raise NotImplementedError()
        if typ == BOOL:
            return self.BOOL
        if typ == INT:
            return self.INT

        w = typ.bit_length()
        assert isinstance(w, int), w

        def add_kw(name, val):
            kw = hdl_map_asoc(HdlValueId(name),
                              HdlValueInt(val, None, None))
            args.append(kw)

        args = [HdlValueInt(w, None, None)]
        if typ.signed is not BITS_DEFAUTL_SIGNED:
            add_kw("signed", typ.signed)
        if typ.force_vector is not BITS_DEFAUTL_FORCEVECTOR and w <= 1:
            add_kw("force_vector", typ.force_vector)
        if typ.negated is not BITS_DEFAUTL_NEGATED:
            add_kw("negated", typ.negated)

        return hdl_call(self.BITS, args)
