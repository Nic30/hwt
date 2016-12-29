from hwt.synthesizer.interfaceLevel.interface import Interface
from hwt.interfaces.std import Signal


class DifferentialSig(Interface):
    def _declr(self):
        self.n = Signal()
        self.p = Signal()
