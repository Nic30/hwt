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

    :ivar ~.force_vector: in order to make this a vector[0] instead of single bit
        use FORCE_VECTOR=True
    """

    def _config(self):
        self.DATA_WIDTH = Param(1)
        self.FORCE_VECTOR = False

    def _declr(self):
        t = Bits(self.DATA_WIDTH, force_vector=self.FORCE_VECTOR)

        # connect
        self.t = Signal(dtype=t)
        # input
        self.i = Signal(dtype=t, masterDir=DIRECTION.IN)
        # output
        self.o = Signal(dtype=t)

    def _initSimAgent(self, sim: HdlSimulator):
        rst = self._getAssociatedRst()
        self._ag = TristateAgent(sim, self, (rst, rst._dtype.negated))


class TristateClk(Clk, TristateSig):
    def _config(self):
        Clk._config(self)
        TristateSig._config(self)

    def _getIpCoreIntfClass(self):
        raise IntfIpMetaNotSpecified()

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = TristateClkAgent(sim, self)
