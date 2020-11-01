from collections import deque

from hwt.simulator.agentBase import SyncAgentBase
from pycocotb.process_utils import OnRisingCallbackLoop
from pycocotb.triggers import Timer, WaitWriteOnly, WaitCombRead, WaitCombStable,\
    WaitTimeslotEnd
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.constants import CLK_PERIOD


class FifoReaderAgent(SyncAgentBase):
    """
    Simulation agent for FifoReader interface
    """

    def __init__(self, sim, intf, allowNoReset=False):
        super(FifoReaderAgent, self).__init__(sim, intf, allowNoReset)
        self.data = deque()
        self.readPending = False
        self.lastData = None

        # flags to keep data coherent when enable state changes
        self.lastData_invalidate = False
        self.readPending_invalidate = False

    def setEnable_asDriver(self, en):
        lastEn = self._enabled
        super(FifoReaderAgent, self).setEnable_asDriver(en)
        self.intf.wait.write(not en)
        self.lastData_invalidate = not en
        if not lastEn:
            self.dataWriter.setEnable(en)

    def setEnable_asMonitor(self, en):
        lastEn = self._enabled
        super(FifoReaderAgent, self).setEnable_asMonitor(en)
        self.intf.en.write(en)
        self.readPending_invalidate = not en
        if not lastEn:
            self.dataReader.setEnable(en)
        # else dataReader will disable itself

    def driver_init(self):
        yield WaitWriteOnly()
        self.intf.wait.write(not self._enabled)

    def monitor_init(self):
        yield WaitWriteOnly()
        self.intf.en.write(self._enabled)

    def get_data(self):
        return self.intf.data.read()

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
        return ([self.monitor_init()] +
                super(FifoReaderAgent, self).getMonitors() +
                [self.dataReader()])

    def monitor(self):
        """
        Initialize data reading if wait is 0
        """
        intf = self.intf
        yield WaitCombRead()
        if self.notReset():
            # wait until wait signal is stable
            wait_last = None
            while True:
                yield WaitCombRead()
                wait = intf.wait.read()
                try:
                    wait = int(wait)
                except ValueError:
                    raise AssertionError(self.sim.now, intf, "wait signal in invalid state")

                if wait is wait_last:
                    break
                else:
                    wait_last = wait
                    yield WaitWriteOnly()

            rd = not wait
        else:
            rd = False

        yield WaitWriteOnly()
        intf.en.write(rd)

        self.readPending = rd

    def getDrivers(self):
        self.dataWriter = OnRisingCallbackLoop(self.sim, self.clk,
                                               self.dataWriter,
                                               self.getEnable)
        return ([self.driver_init()] +
                super(FifoReaderAgent, self).getDrivers() +
                [self.dataWriter()])

    def set_data(self, d):
        self.intf.data.write(d)

    def dataWriter(self):
        # delay data litle bit to have nicer wave
        # otherwise wirte happens before next clk period
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
        intf = self.intf
        yield WaitCombRead()
        rst_n = self.notReset()
        # speculative write
        if rst_n and self.data:
            wait = 0
        else:
            wait = 1

        yield WaitWriteOnly()
        intf.wait.write(wait)

        if rst_n:
            # wait for potential update of en
            # check if write can be performed and if it possible do real write
            yield WaitTimeslotEnd()
            en = intf.en.read()
            try:
                en = int(en)
            except ValueError:
                raise AssertionError(self.sim.now, intf,
                                     "en signal in invalid state")

            if en:
                assert self.data, (self.sim.now, intf, "underflow")
                self.lastData = self.data.popleft()


class FifoWriterAgent(SyncAgentBase):
    """
    Simulation agent for FifoWriter interface
    """

    def __init__(self, sim: HdlSimulator, intf, allowNoReset=False):
        super(FifoWriterAgent, self).__init__(
            sim, intf, allowNoReset=allowNoReset)
        self.data = deque()

    def driver_init(self):
        yield WaitWriteOnly()
        self.intf.en.write(self._enabled)

    def monitor_init(self):
        yield WaitWriteOnly()
        self.intf.wait.write(not self._enabled)

    def setEnable_asDriver(self, en):
        SyncAgentBase.setEnable_asDriver(self, en)
        self.intf.en.write(en)

    def setEnable_asMonitor(self, en):
        SyncAgentBase.setEnable_asMonitor(self, en)
        self.intf.wait.write(not en)

    def get_data(self):
        return self.intf.data.read()

    def set_data(self, d):
        self.intf.data.write(d)

    def monitor(self):
        # set wait signal
        # if en == 1 take data
        intf = self.intf
        yield WaitWriteOnly()
        intf.wait.write(0)

        yield WaitCombStable()
        # wait for potential update of en

        en = intf.en.read()
        try:
            en = int(en)
        except ValueError:
            raise AssertionError(self.sim.now, intf,
                                 "en signal in invalid state")

        if en:
            yield Timer(CLK_PERIOD // 10)
            yield WaitCombRead()
            self.data.append(self.get_data())

    def driver(self):
        # if wait == 0 set en=1 and set data
        intf = self.intf

        d = None
        v = 0
        yield WaitCombRead()
        if self.notReset() and self.data:
            yield WaitCombRead()

            wait = intf.wait.read()
            try:
                wait = int(wait)
            except ValueError:
                raise AssertionError(self.sim.now, intf,
                                     "wait signal in invalid state")
            if not wait:
                d = self.data.popleft()
                v = 1

        yield WaitWriteOnly()
        self.set_data(d)
        intf.en.write(v)

    def getDrivers(self):
        return SyncAgentBase.getDrivers(self) + [self.driver_init()]

    def getMonitors(self):
        return SyncAgentBase.getMonitors(self) + [self.monitor_init()]
