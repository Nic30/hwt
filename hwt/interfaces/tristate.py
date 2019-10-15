from hwt.hdl.constants import DIRECTION
from hwt.hdl.types.bits import Bits
from hwt.interfaces.std import Signal, Clk
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.param import Param
from ipCorePackager.intfIpMeta import IntfIpMetaNotSpecified
from pycocotb.agents.peripheral.tristate import TristateAgent, TristateClkAgent
from pycocotb.hdlSimulator import HdlSimulator


class TristateSig(Interface):
    """
    Tristate interface
    in order to make this a vector[0] instead of single bit
    use force_vector=True
    """

    def _config(self):
        self.DATA_WIDTH = Param(1)
        self.force_vector = False

    def _declr(self):
        t = Bits(self.DATA_WIDTH, self.force_vector)

        # connect
        self.t = Signal(dtype=t)
        # input
        self.i = Signal(dtype=t, masterDir=DIRECTION.IN)
        # output
        self.o = Signal(dtype=t)

    def _initSimAgent(self, sim: HdlSimulator):
        # [todo] missing mapping of signals
        self._ag = TristateAgent(self)


class TristateClk(Clk, TristateSig):
    def _getIpCoreIntfClass(self):
        raise IntfIpMetaNotSpecified()

    def _initSimAgent(self, sim: HdlSimulator):
        # [todo] missing mapping of signals
        self._ag = TristateClkAgent(sim, self)
