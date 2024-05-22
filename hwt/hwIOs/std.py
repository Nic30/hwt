from typing import TypeVar, Generic, Union, Optional, Dict

from hwt.hwIO import HwIO
from hwt.hwIOs.agents.bramPort import HwIOBramPortAgent
from hwt.hwIOs.agents.bramPort import HwIOBramPort_noClkAgent
from hwt.hwIOs.agents.fifo import HwIOFifoReaderAgent
from hwt.hwIOs.agents.fifo import HwIOFifoWriterAgent
from hwt.hwIOs.agents.rdSync import HwIODataRdAgent
from hwt.hwIOs.agents.rdVldSync import HwIORdVldSyncAgent, HwIODataRdVldAgent
from hwt.hwIOs.agents.regCntrl import HwIORegCntrlAgent
from hwt.hwIOs.agents.signal import HwIOSignalAgent
from hwt.hwIOs.agents.vldSync import HwIODataVldAgent
from hwt.hwIOs.signalOps import SignalOps
from hwt.hwParam import HwParam
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BIT, BIT_N
from hwt.hdl.types.hdlType import HdlType
from hwtSimApi.agents.clk import ClockAgent
from hwtSimApi.agents.rst import PullDownAgent
from hwtSimApi.agents.rst import PullUpAgent
from hwtSimApi.hdlSimulator import HdlSimulator
from hwtSimApi.utils import freq_to_period
from ipCorePackager.constants import DIRECTION


T = TypeVar("T", bound=HdlType)


class HwIOSignal(SignalOps, HwIO, Generic[T]):
    """
    Basic wire interface

    :ivar ~._dtype: type of signal
    :ivar ~._sig: RtlSignal instance (physical representation of this logical signal)
    :ivar ~._sigInside: _sig after to_rtl conversion is made
        (after to_rtl conversion _sig is signal for parent module
        and _sigInside is signal in original module, this separates process
        of translating modules)
    :note: _sigInside is None if the body of component was not elaborated yet
    :ivar _isAccessible: flag which is set False if the signal is inside of some elaborated module
    """

    def __init__(self,
                 dtype: HdlType=BIT,
                 masterDir: DIRECTION=DIRECTION.OUT,
                 hdl_name:Optional[Union[str, Dict[str, str]]]=None,
                 loadConfig: bool=True):
        self._sig: Optional["RtlSignal"] = None
        self._sigInside: Optional["RtlSignal"] = None
        self._isAccessible = True
        super().__init__(masterDir=masterDir,
                         hdl_name=hdl_name,
                         loadConfig=loadConfig)
        self._dtype = dtype

    def _clean(self, lockNonExternal=True):
        """
        :see: :func:`HwIO._clean`
        """
        self._sigInside = self._sig
        self._sig = None
        if lockNonExternal and not self._isExtern:
            self._isAccessible = False
        if self._hwIOs:
            HwIO._clean(self, lockNonExternal=lockNonExternal)

    def __copy__(self):
        """
        Create new instance of interface of same type and configuration
        """
        hwIO = self.__class__(masterDir=self._masterDir,
                              dtype=self._dtype)
        hwIO._updateParamsFrom(self)
        return hwIO

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIOSignalAgent(sim, self)


def HwIOVectSignal(width: int,
               signed: Union[bool, None]=None,
               masterDir=DIRECTION.OUT,
               hdl_name:Optional[Union[str, Dict[str, str]]]=None,
               loadConfig=True):
    """
    Create basic :class:`.HwIOSignal` interface where type is vector
    """
    return HwIOSignal(HBits(width, signed, force_vector=True),
                  masterDir,
                  hdl_name,
                  loadConfig)


class HwIOClk(HwIOSignal):
    """
    Basic :class:`.HwIOSignal` interface which is interpreted as clock signal
    """
    DEFAULT_FREQ = int(100e6)

    def _config(self):
        self.FREQ = HwParam(HwIOClk.DEFAULT_FREQ)

    def _getIpCoreIntfClass(self):
        from hwt.hwIOs.std_ip_defs import IP_Clk
        return IP_Clk

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = ClockAgent(sim, self, period=int(freq_to_period(self.FREQ)))


class HwIORst(HwIOSignal[HBits]):
    """
    Basic :class:`.HwIOSignal` interface which is interpreted as reset signal
    """

    def _getIpCoreIntfClass(self):
        from hwt.hwIOs.std_ip_defs import IP_Rst
        return IP_Rst

    def _initSimAgent(self, sim: HdlSimulator):
        clk = self._getAssociatedClk()
        self._ag = PullDownAgent(sim, self,
                                 initDelay=int(0.6 * freq_to_period(clk.FREQ)))


class HwIORst_n(HwIOSignal[HBits]):
    """
    Basic :class:`.HwIOSignal` interface which is interpreted as reset signal
    with negative polarity (active in 0)
    """

    def __init__(self,
                 masterDir=DIRECTION.OUT,
                 dtype=BIT_N,
                 hdl_name:Optional[Union[str, Dict[str, str]]]=None,
                 loadConfig=True):
        super(HwIORst_n, self).__init__(masterDir=masterDir,
                                    dtype=dtype,
                                    hdl_name=hdl_name,
                                    loadConfig=loadConfig)

    def _getIpCoreIntfClass(self):
        from hwt.hwIOs.std_ip_defs import IP_Rst_n
        return IP_Rst_n

    def _initSimAgent(self, sim: HdlSimulator):
        clk = self._getAssociatedClk()
        self._ag = PullUpAgent(sim, self,
                               initDelay=int(0.6 * freq_to_period(clk.FREQ)))


class HwIOVldSync(HwIO):

    def _declr(self):
        self.vld = HwIOSignal()


class HwIODataVld(HwIOVldSync):
    """
    HwIO data+valid signal, if vld=1 then data are valid and slave should
    accept them
    """

    def _config(self):
        self.DATA_WIDTH = HwParam(64)

    def _declr(self):
        self.data = HwIOVectSignal(self.DATA_WIDTH)
        HwIOVldSync._declr(self)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIODataVldAgent(sim, self)


class HwIORdSync(HwIO):

    def _declr(self) -> None:
        self.rd = HwIOSignal(masterDir=DIRECTION.IN)


class HwIODataRd(HwIORdSync):
    """
    HwIO data+ready signal, if rd=1 then slave has read data and master
    should actualize data
    """

    def _config(self):
        self.DATA_WIDTH = HwParam(64)

    def _declr(self):
        self.data = HwIOVectSignal(self.DATA_WIDTH)
        HwIORdSync._declr(self)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIODataRdAgent(sim, self)


class HwIORdVldSync(HwIO):
    """
    Only synchronization interface, like vld+rd signal with meaning
    like in :class:`.HwIODataRdVld` interface

    :ivar ~.rd: when high slave is ready to receive data
    :ivar ~.vld: when high master is sending data to slave

    transaction happens when both ready and valid are high
    """

    def _declr(self):
        HwIOVldSync._declr(self)
        HwIORdSync._declr(self)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIORdVldSyncAgent(sim, self)


class HwIODataRdVld(HwIORdVldSync):
    """
    HwIO data+ready+valid signal, if rd=1 slave is ready to accept data,
    if vld=1 master is sending data,
    if rd=1 and vld=1 then data is transfered otherwise master
    and slave has to wait on each other

    :attention: one rd/vld is set it must not go down until transaction is made
    """

    def _config(self):
        self.DATA_WIDTH = HwParam(64)

    def _declr(self):
        HwIODataVld._declr(self)
        HwIORdSync._declr(self)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIODataRdVldAgent(sim, self)


class HwIOReqDoneSync(HwIO):
    """
    Synchronization interface, if req=1 slave begins operation and when
    it's done it asserts done=1 for one clk tick req does not need to stay high

    AMBA CXS Protocol Specification https://developer.arm.com/documentation/ihi0079/latest/  (req=CXSVALID, done=CXSCRDGNT)
    """

    def _config(self) -> None:
        self.CREDIT_CNT = HwParam(1)

    def _declr(self):
        self.req = HwIOSignal()
        self.done = HwIOSignal(masterDir=DIRECTION.IN)


class HwIOBramPort_noClk(HwIO):
    """
    Basic BRAM port
    """

    def _config(self):
        self.ADDR_WIDTH = HwParam(32)
        self.DATA_WIDTH = HwParam(64)
        self.HAS_R = HwParam(True)
        self.HAS_W = HwParam(True)
        self.HAS_BE = HwParam(False)

    def _declr(self):
        assert self.HAS_R or self.HAS_W, "has to have at least read or write part"

        self.addr = HwIOVectSignal(self.ADDR_WIDTH)
        DATA_WIDTH = self.DATA_WIDTH
        if self.HAS_W:
            self.din = HwIOVectSignal(DATA_WIDTH)

        if self.HAS_R:
            self.dout = HwIOVectSignal(DATA_WIDTH, masterDir=DIRECTION.IN)

        self.en = HwIOSignal()
        if (self.HAS_R and self.HAS_W) or (self.HAS_W and self.HAS_BE):
            # in write only mode we do not need this as well as we can use "en"
            if self.HAS_BE:
                assert DATA_WIDTH % 8 == 0, DATA_WIDTH
                self.we = HwIOVectSignal(DATA_WIDTH // 8)
            else:
                self.we = HwIOSignal()

    def _getWordAddrStep(self):
        """
        :return: size of one word in module of address
        """
        return 1

    def _getAddrStep(self):
        """
        :return: how many bits is one module of address (e.g. 8 bits for
            char * pointer, 36 for 36 bit bram)
        """
        return int(self.DATA_WIDTH)

    def _getIpCoreIntfClass(self):
        from hwt.hwIOs.std_ip_defs import IP_BlockRamPort
        return IP_BlockRamPort

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIOBramPort_noClkAgent(sim, self)


class HwIOBramPort(HwIOBramPort_noClk):
    """
    BRAM port with it's own clk
    """

    def _declr(self):
        self.clk = HwIOSignal(masterDir=DIRECTION.OUT)
        with self._associated(clk=self.clk):
            super()._declr()

        self._make_association(clk=self.clk)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIOBramPortAgent(sim, self)


class HwIOFifoWriter(HwIO):
    """
    FIFO write port interface
    """

    def _config(self):
        self.DATA_WIDTH = HwParam(8)

    def _declr(self):
        self.en = HwIOSignal()
        self.wait = HwIOSignal(masterDir=DIRECTION.IN)
        if self.DATA_WIDTH:
            self.data = HwIOVectSignal(self.DATA_WIDTH)

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIOFifoWriterAgent(sim, self)

    def _getIpCoreIntfClass(self):
        from hwt.hwIOs.std_ip_defs import IP_FifoWriter
        return IP_FifoWriter


class HwIOFifoReader(HwIO):
    """
    FIFO read port interface
    """

    def _config(self):
        HwIOFifoWriter._config(self)

    def _declr(self):
        HwIOFifoWriter._declr(self)
        self.en._masterDir = DIRECTION.IN
        self.wait._masterDir = DIRECTION.OUT

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIOFifoReaderAgent(sim, self)

    def _getIpCoreIntfClass(self):
        from hwt.hwIOs.std_ip_defs import IP_FifoReader
        return IP_FifoReader


class HwIORegCntrl(HwIO):
    """
    Register control interface, :class:`.HwIOSignal` for read, :class:`.HwIODataVld`
    for write
    """

    def _config(self):
        self.DATA_WIDTH = HwParam(8)
        self.USE_IN = HwParam(True)
        self.USE_OUT = HwParam(True)

    def _declr(self):
        if self.USE_IN:
            self.din = HwIOVectSignal(self.DATA_WIDTH, masterDir=DIRECTION.IN)
        if self.USE_OUT:
            with self._hwParamsShared():
                self.dout = HwIODataVld()

    def _initSimAgent(self, sim: HdlSimulator):
        self._ag = HwIORegCntrlAgent(sim, self)
