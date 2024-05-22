from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from pyMathBitPrecise.floatt import Floatt


class HFloat(HdlType, Floatt):
    """
    Elemental HDL type representing IEEE 754 like float type.
    """

    def __init__(self, exponent_w, mantisa_w,
                 name=None,
                 const=False):
        """
        :param negated: if true the value is in negated form
        """
        HdlType.__init__(self, const=const)
        assert exponent_w > 0, exponent_w
        assert mantisa_w > 0, mantisa_w
        Floatt.__init__(self, exponent_w, mantisa_w, name=name)

    @internal
    @classmethod
    def getConstCls(cls):
        from hwt.hdl.types.floatConst import HFloatConst
        return HFloatConst

