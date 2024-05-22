from hwt.hdl.types.bits import HBits
from hwt.hwIO import HwIO
from hwt.hwIOs.std import HwIOSignal, HwIOClk
from hwt.hwParam import HwParam
from hwt.pyUtils.typingFuture import override
from hwtSimApi.agents.peripheral.tristate import TristateAgent, TristateClkAgent
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import DIRECTION
from ipCorePackager.intfIpMeta import IntfIpMetaNotSpecifiedError


class HwIOTristateSig(HwIO):
    """
    Tristate interface

    :ivar ~.force_vector: in order to make this a vector[0] instead of single bit
        use FORCE_VECTOR=True
    """

    @override
    def _config(self):
        self.DATA_WIDTH = HwParam(1)
        self.FORCE_VECTOR = False

    @override
    def _declr(self):
        t = HBits(self.DATA_WIDTH, force_vector=self.FORCE_VECTOR)

        # connect
        self.t = HwIOSignal(dtype=t)
        # input
        self.i = HwIOSignal(dtype=t, masterDir=DIRECTION.IN)
        # output
        self.o = HwIOSignal(dtype=t)

    @override
    def _initSimAgent(self, sim: HdlSimulator):
        rst = self._getAssociatedRst()
        self._ag = TristateAgent(sim, self, (rst, rst._dtype.negated))


class HwIOTristateClk(HwIOClk, HwIOTristateSig):

    @override
    def _config(self):
        HwIOClk._config(self)
        HwIOTristateSig._config(self)

    @override
    def _getIpCoreIntfClass(self):
        raise IntfIpMetaNotSpecifiedError()

    @override
    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = TristateClkAgent(sim, self)
