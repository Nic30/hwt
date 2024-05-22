from hwt.hwIO import HwIO
from hwt.hwIOs.std import HwIOSignal
from hwt.hdl.types.bits import HBits


class HwIODifferentialSig(HwIO):
    """
    HwIO of differential pair
    """

    def _declr(self):
        self.n = HwIOSignal(dtype=HBits(1, negated=True))
        self.p = HwIOSignal()
