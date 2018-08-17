from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal
from hwt.synthesizer.interface import Interface


class DifferentialSig(Interface):

    def _declr(self):
        self.n = Signal(dtype=Bits(1, negated=1))
        self.p = Signal()
