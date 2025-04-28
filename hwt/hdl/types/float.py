from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.pyUtils.typingFuture import override
from pyMathBitPrecise.floatt import Floatt


class HFloat(HdlType, Floatt):
    """
    Basic HDL type representing IEEE 754 like float type.

    :note: This type is meant for HwModule parameters, operations with this type are not synthetisable.
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
    @override
    @classmethod
    def getConstCls(cls):
        from hwt.hdl.types.floatConst import HFloatConst
        return HFloatConst

    @internal
    @override
    @classmethod
    def getRtlSignalCls(cls):
        from hwt.hdl.types.floatConst import HFloatRtlSignal
        return HFloatRtlSignal

