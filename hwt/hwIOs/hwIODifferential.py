from hwt.hdl.types.bits import HBits
from hwt.hwIO import HwIO
from hwt.hwIOs.std import HwIOSignal
from hwt.pyUtils.typingFuture import override


class HwIODifferentialSig(HwIO):
    """
    HwIO of differential pair
    """

    @override
    def hwDeclr(self):
        self.n = HwIOSignal(dtype=HBits(1, negated=True))
        self.p = HwIOSignal()
