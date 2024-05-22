from collections import deque

from hwt.simulator.agentBase import SyncAgentBase
from hwtSimApi.constants import CLK_PERIOD
from hwtSimApi.hdlSimulator import HdlSimulator
from hwtSimApi.process_utils import OnRisingCallbackLoop
from hwtSimApi.triggers import Timer, WaitWriteOnly, WaitCombRead, WaitCombStable, \
    WaitTimeslotEnd


class HwIOFifoReaderAgent(SyncAgentBase):
    """
    Simulation agent for FifoReader interface
    """

    def __init__(self, sim: HdlSimulator, hwIO: "HwIOFifoReader", allowNoReset=False):
        super(HwIOFifoReaderAgent, self).__init__(sim, hwIO, allowNoReset)
        self.data = deque()
        self.readPending = False
        self.lastData = None

        # flags to keep data coherent when enable state changes
        self.lastData_invalidate = False
        self.readPending_invalidate = False
        if hwIO.DATA_WIDTH == 0:
            raise NotImplementedError()

    def setEnable_asDriver(self, en: bool):
        lastEn = self._enabled
        super(HwIOFifoReaderAgent, self).setEnable_asDriver(en)
        self.hwIO.wait.write(not en)
        self.lastData_invalidate = not en
        if not lastEn:
            self.dataWriter.setEnable(en)

    def setEnable_asMonitor(self, en: bool):
        lastEn = self._enabled
        super(HwIOFifoReaderAgent, self).setEnable_asMonitor(en)
        self.hwIO.en.write(en)
        self.readPending_invalidate = not en
        if not lastEn:
            self.dataReader.setEnable(en)
        # else dataReader will disable itself

    def driver_init(self):
        yield WaitWriteOnly()
        self.hwIO.wait.write(not self._enabled)

    def monitor_init(self):
        yield WaitWriteOnly()
        self.hwIO.en.write(self._enabled)

    def get_data(self):
        return self.hwIO.data.read()

    def dataReader(self):
        yield Timer(1)
        if self.readPending:
            yield WaitCombRead()
            d = self.get_data()
            self.data.append(d)

            if self.readPending_invalidate:
                self.readPending = False
        if not self.readPending and not self._enabled:
            self.dataWriter.setEnable(False)

    def getMonitors(self):
        self.dataReader = OnRisingCallbackLoop(self.sim, self.clk,
                                               self.dataReader,
                                               self.getEnable)
        yield self.monitor_init()
        yield from super(HwIOFifoReaderAgent, self).getMonitors()
        yield self.dataReader()

    def monitor(self):
        """
        Initialize data reading if wait is 0
        """
        hwIO = self.hwIO
        yield WaitCombRead()
        if self.notReset():
            # wait until wait signal is stable
            wait_last = None
            while True:
                yield WaitCombRead()
                wait = hwIO.wait.read()
                try:
                    wait = int(wait)
                except ValueError:
                    raise AssertionError(self.sim.now, hwIO, "wait signal in invalid state")

                if wait is wait_last:
                    break
                else:
                    wait_last = wait
                    yield WaitWriteOnly()

            rd = not wait
        else:
            rd = False

        yield WaitWriteOnly()
        hwIO.en.write(rd)

        self.readPending = rd

    def getDrivers(self):
        self.dataWriter = OnRisingCallbackLoop(self.sim, self.clk,
                                               self.dataWriter,
                                               self.getEnable)
        yield self.driver_init()
        yield from super(HwIOFifoReaderAgent, self).getDrivers()
        yield self.dataWriter()

    def set_data(self, d):
        self.hwIO.data.write(d)

    def dataWriter(self):
        # delay data litle bit to have nicer wave
        # otherwise write happens before next clk period
        # and it means in 0 time and we will not be able to see it in wave
        yield Timer(1)
        yield WaitWriteOnly()
        self.set_data(self.lastData)
        if self.lastData_invalidate:
            self.lastData = None

        if not self._enabled:
            self.dataWriter.setEnable(False)

    def driver(self):
        # now we are before clock event
        # * set wait signal
        # * set last data (done in separate process)
        # * if en == 1, pop next data for next clk
        hwIO = self.hwIO
        yield WaitCombRead()
        rst_n = self.notReset()
        # speculative write
        if rst_n and self.data:
            wait = 0
        else:
            wait = 1

        yield WaitWriteOnly()
        hwIO.wait.write(wait)

        if rst_n:
            # wait for potential update of en
            # check if write can be performed and if it possible do real write
            yield WaitTimeslotEnd()
            en = hwIO.en.read()
            try:
                en = int(en)
            except ValueError:
                raise AssertionError(self.sim.now, hwIO,
                                     "en signal in invalid state")

            if en:
                assert self.data, (self.sim.now, hwIO, "underflow")
                self.lastData = self.data.popleft()


class HwIOFifoWriterAgent(SyncAgentBase):
    """
    Simulation agent for FifoWriter interface
    """

    def __init__(self, sim: HdlSimulator, hwIO: "HwIOFifoWriter", allowNoReset=False):
        super(HwIOFifoWriterAgent, self).__init__(
            sim, hwIO, allowNoReset=allowNoReset)
        self.data = deque()
        if hwIO.DATA_WIDTH == 0:
            raise NotImplementedError()

    def driver_init(self):
        yield WaitWriteOnly()
        self.hwIO.en.write(self._enabled)

    def monitor_init(self):
        yield WaitWriteOnly()
        self.hwIO.wait.write(not self._enabled)

    def setEnable_asDriver(self, en: bool):
        SyncAgentBase.setEnable_asDriver(self, en)
        self.hwIO.en.write(en)

    def setEnable_asMonitor(self, en: bool):
        SyncAgentBase.setEnable_asMonitor(self, en)
        self.hwIO.wait.write(not en)

    def get_data(self):
        return self.hwIO.data.read()

    def set_data(self, d):
        self.hwIO.data.write(d)

    def monitor(self):
        # set wait signal
        # if en == 1 take data
        hwIO = self.hwIO
        yield WaitWriteOnly()
        hwIO.wait.write(0)

        yield WaitCombStable()
        # wait for potential update of en

        en = hwIO.en.read()
        try:
            en = int(en)
        except ValueError:
            raise AssertionError(self.sim.now, hwIO,
                                 "en signal in invalid state")

        if en:
            yield Timer(CLK_PERIOD // 10)
            yield WaitCombRead()
            self.data.append(self.get_data())

    def driver(self):
        # if wait == 0 set en=1 and set data
        hwIO = self.hwIO

        d = None
        v = 0
        yield WaitCombRead()
        if self.notReset() and self.data:
            yield WaitCombRead()

            wait = hwIO.wait.read()
            try:
                wait = int(wait)
            except ValueError:
                raise AssertionError(self.sim.now, hwIO,
                                     "wait signal in invalid state")
            if not wait:
                d = self.data.popleft()
                v = 1

        yield WaitWriteOnly()
        self.set_data(d)
        hwIO.en.write(v)

    def getDrivers(self):
        yield from SyncAgentBase.getDrivers(self)
        yield self.driver_init()

    def getMonitors(self):
        yield from SyncAgentBase.getMonitors(self)
        yield self.monitor_init()
