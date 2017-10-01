from hwt.synthesizer.interfaceLevel.interface import Interface
from hwt.synthesizer.param import Param
from hwt.interfaces.std import Signal, Clk
from hwt.hdl.types.bits import Bits
from hwt.hdl.constants import DIRECTION


class TristateSig(Interface):
    """
    Tristate interface
    in order to make this a vector[0] instead of single bit use forceVector=True
    """
    def _config(self):
        self.DATA_WIDTH = Param(1)
        self.forceVector = False

    def _declr(self):
        t = Bits(self.DATA_WIDTH, self.forceVector)

        # connect
        self.t = Signal(dtype=t)
        # input
        self.i = Signal(dtype=t, masterDir=DIRECTION.IN)
        # output
        self.o = Signal(dtype=t)


class TristateClk(Clk, TristateSig):
    def _getIpCoreIntfClass(self):
        raise NotImplementedError()

    def _getSimAgent(self):
        raise NotImplementedError()
