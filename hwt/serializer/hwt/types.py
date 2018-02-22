from hwt.hdl.types.integerVal import IntegerVal
from hwt.synthesizer.param import evalParam
from hwt.serializer.simModel.types import SimModelSerializer_types


class HwtSerializer_types(SimModelSerializer_types):
    """
    part of SimModelSerializer responsible for type serialization
    """

    @classmethod
    def HdlType_int(cls, typ, ctx, declaration):
        if declaration:
            raise NotImplementedError()
        return "INT"

    @classmethod
    def HdlType_bits(cls, typ, ctx, declaration=False):
        if declaration:
            raise NotImplementedError()
        w = typ.width
        if isinstance(w, int):
            pass
        else:
            w = evalParam(w)
            assert isinstance(w, IntegerVal)
            assert w._isFullVld()
            w = w.val

        return "Bits(%d, signed=%r, forceVector=%r, negated=%r)" % (
            w, typ.signed, typ.forceVector, typ.negated)
