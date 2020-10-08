from hwt.hdl.constants import DIRECTION
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BIT, BIT_N
from hwt.interfaces.agents.bramPort import BramPortAgent
from hwt.interfaces.agents.bramPort import BramPort_withoutClkAgent
from hwt.interfaces.agents.fifo import FifoReaderAgent
from hwt.interfaces.agents.fifo import FifoWriterAgent
from hwt.interfaces.agents.handshaked import HandshakeSyncAgent
from hwt.interfaces.agents.handshaked import HandshakedAgent
from hwt.interfaces.agents.rdSynced import RdSyncedAgent
from hwt.interfaces.agents.regCntrl import RegCntrlAgent
from hwt.interfaces.agents.signal import SignalAgent
from hwt.interfaces.agents.vldSynced import VldSyncedAgent
from hwt.interfaces.signalOps import SignalOps
from hwt.synthesizer.interface import Interface
from hwt.synthesizer.param import Param
from pycocotb.agents.clk import ClockAgent
from pycocotb.agents.rst import PullDownAgent
from pycocotb.agents.rst import PullUpAgent
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.utils import freq_to_period


D = DIRECTION


class Signal(SignalOps, Interface):
    """
    Basic wire interface

    :ivar ~._dtype: type of signal
    :ivar ~._sig: RtlSignal instance (physical representation of this logical signal)
    :ivar ~._sigInside: _sig after to_rtl conversion is made
        (after to_rtl conversion _sig is signal for parent unit
        and _sigInside is signal in original unit, this separates process
        of translating units)
    :note: _sigInside is None if the body of component was not elaborated yet
    :ivar _isAccessible: flag which is set False if the signal is inside of some elaborated unit
    """

    def __init__(self,
                 masterDir=D.OUT,
                 dtype=BIT,
                 loadConfig=True):
        self._sig = None
        self._sigInside = None
        self._isAccessible = True
        super().__init__(masterDir=masterDir,
                         loadConfig=loadConfig)
        self._dtype = dtype

    def _clean(self, lockNonExternal=True):
        """
        :see: :func:`Interface._clean`
        """
        self._sigInside = self._sig
        self._sig = None
        if lockNonExternal and not self._isExtern:
            self._isAccessible = False
        if self._interfaces:
            Interface._clean(self, lockNonExternal=lockNonExternal)

    def __copy__(self):
        """
        Create new instance of interface of same type and configuration
        """
        intf = self.__class__(masterDir=self._masterDir,
                              dtype=self._dtype)
        intf._updateParamsFrom(self)
        return intf

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = SignalAgent(sim, self)


def VectSignal(width,
               signed=None,
               masterDir=D.OUT,
               loadConfig=True):
    """
    Create basic :class:`.Signal` interface where type is vector
    """
    return Signal(masterDir,
                  Bits(width, signed, force_vector=True),
                  loadConfig)


class Clk(Signal):
    """
    Basic :class:`.Signal` interface which is interpreted as clock signal
    """
    DEFAULT_FREQ = int(100e6)

    def _config(self):
        self.FREQ = Param(self.DEFAULT_FREQ)

    def _getIpCoreIntfClass(self):
        from hwt.interfaces.std_ip_defs import IP_Clk
        return IP_Clk

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = ClockAgent(sim, self, period=int(freq_to_period(self.FREQ)))


class Rst(Signal):
    """
    Basic :class:`.Signal` interface which is interpreted as reset signal
    """

    def _getIpCoreIntfClass(self):
        from hwt.interfaces.std_ip_defs import IP_Rst
        return IP_Rst

    def _initSimAgent(self, sim: HdlSimulator):
        clk = self._getAssociatedClk()
        self._ag = PullDownAgent(sim, self,
                                 initDelay=int(0.6 * freq_to_period(clk.FREQ)))


class Rst_n(Signal):
    """
    Basic :class:`.Signal` interface which is interpreted as reset signal
    with negative polarity (active in 0)
    """

    def __init__(self,
                 masterDir=D.OUT,
                 dtype=BIT_N,
                 loadConfig=True):
        super(Rst_n, self).__init__(masterDir=masterDir,
                                    dtype=dtype,
                                    loadConfig=loadConfig)

    def _getIpCoreIntfClass(self):
        from hwt.interfaces.std_ip_defs import IP_Rst_n
        return IP_Rst_n

    def _initSimAgent(self, sim: HdlSimulator):
        clk = self._getAssociatedClk()
        self._ag = PullUpAgent(sim, self,
                               initDelay=int(0.6 * freq_to_period(clk.FREQ)))


class VldSynced(Interface):
    """
    Interface data+valid signal, if vld=1 then data are valid and slave should
    accept them
    """

    def _config(self):
        self.DATA_WIDTH = Param(64)

    def _declr(self):
        self.data = VectSignal(self.DATA_WIDTH)
        self.vld = Signal()

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = VldSyncedAgent(sim, self)


class RdSynced(Interface):
    """
    Interface data+ready signal, if rd=1 then slave has read data and master
    should actualize data
    """

    def _config(self):
        self.DATA_WIDTH = Param(64)

    def _declr(self):
        self.data = VectSignal(self.DATA_WIDTH)
        self.rd = Signal(masterDir=D.IN)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = RdSyncedAgent(sim, self)


class Handshaked(VldSynced):
    """
    Interface data+ready+valid signal, if rd=1 slave is ready to accept data,
    if vld=1 master is sending data,
    if rd=1 and vld=1 then data is transfered otherwise master
    and slave has to wait on each other

    :attention: one rd/vld is set it must not go down until transaction is made
    """

    def _declr(self):
        super()._declr()
        self.rd = Signal(masterDir=D.IN)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HandshakedAgent(sim, self)


class HandshakeSync(Interface):
    """
    Only synchronization interface, like vld+rd signal with meaning
    like in :class:`.Handshaked` interface

    :ivar ~.rd: when high slave is ready to receive data
    :ivar ~.vld: when high master is sending data to slave

    transaction happens when both ready and valid are high

    """

    def _declr(self):
        self.vld = Signal()
        self.rd = Signal(masterDir=D.IN)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HandshakeSyncAgent(sim, self)


class ReqDoneSync(Interface):
    """
    Synchronization interface, if req=1 slave begins operation and when
    it's done it asserts done=1 for one clk tick req does not need to stay high
    """

    def _declr(self):
        self.req = Signal()
        self.done = Signal(masterDir=D.IN)


class BramPort_withoutClk(Interface):
    """
    Basic BRAM port
    """

    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64)
        self.HAS_R = Param(True)
        self.HAS_W = Param(True)
        self.HAS_BE = Param(False)

    def _declr(self):
        assert self.HAS_R or self.HAS_W, "has to have at least read or write part"

        self.addr = VectSignal(self.ADDR_WIDTH)
        DATA_WIDTH = self.DATA_WIDTH
        if self.HAS_W:
            self.din = VectSignal(DATA_WIDTH)

        if self.HAS_R:
            self.dout = VectSignal(DATA_WIDTH, masterDir=D.IN)

        self.en = Signal()
        if (self.HAS_R and self.HAS_W) or (self.HAS_W and self.HAS_BE):
            # in write only mode we do not need this as well as we can use "en"
            if self.HAS_BE:
                assert DATA_WIDTH % 8 == 0, DATA_WIDTH
                self.we = VectSignal(DATA_WIDTH // 8)
            else:
                self.we = Signal()

    def _getWordAddrStep(self):
        """
        :return: size of one word in unit of address
        """
        return 1

    def _getAddrStep(self):
        """
        :return: how many bits is one unit of address (f.e. 8 bits for
            char * pointer, 36 for 36 bit bram)
        """
        return int(self.DATA_WIDTH)

    def _getIpCoreIntfClass(self):
        from hwt.interfaces.std_ip_defs import IP_BlockRamPort
        return IP_BlockRamPort

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = BramPort_withoutClkAgent(sim, self)


class BramPort(BramPort_withoutClk):
    """
    BRAM port with it's own clk
    """

    def _declr(self):
        self.clk = Signal(masterDir=D.OUT)
        with self._associated(clk=self.clk):
            super()._declr()

        self._make_association(clk=self.clk)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = BramPortAgent(sim, self)


class FifoWriter(Interface):
    """
    FIFO write port interface
    """
    def _config(self):
        self.DATA_WIDTH = Param(8)

    def _declr(self):
        self.en = Signal()
        self.wait = Signal(masterDir=D.IN)
        self.data = VectSignal(self.DATA_WIDTH)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = FifoWriterAgent(sim, self)

    def _getIpCoreIntfClass(self):
        from hwt.interfaces.std_ip_defs import IP_FifoWriter
        return IP_FifoWriter


class FifoReader(FifoWriter):
    """
    FIFO read port interface
    """
    def _declr(self):
        super()._declr()
        self.en._masterDir = D.IN
        self.wait._masterDir = D.OUT

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = FifoReaderAgent(sim, self)

    def _getIpCoreIntfClass(self):
        from hwt.interfaces.std_ip_defs import IP_FifoReader
        return IP_FifoReader


class RegCntrl(Interface):
    """
    Register control interface, :class:`.Signal` for read, :class:`.VldSynced`
    for write
    """

    def _config(self):
        self.DATA_WIDTH = Param(8)
        self.USE_IN = Param(True)
        self.USE_OUT = Param(True)

    def _declr(self):
        if self.USE_IN:
            self.din = VectSignal(self.DATA_WIDTH, masterDir=D.IN)
        if self.USE_OUT:
            with self._paramsShared():
                self.dout = VldSynced()

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = RegCntrlAgent(sim, self)
