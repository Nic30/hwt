from collections import deque

from hwt.simulator.agentBase import SyncAgentBase
from hwt.simulator.shortcuts import OnRisingCallbackLoop
from hwt.interfaces.agents.signal import DEFAULT_CLOCK
from hwt.simulator.hdlSimulator import Timer


class FifoReaderAgent(SyncAgentBase):
    """
    Simulation agent for FifoReader interface
    """

    def __init__(self, intf, allowNoReset=False):
        super(FifoReaderAgent, self).__init__(intf, allowNoReset)
        self.data = deque()
        self.readPending = False
        self.lastData = None

        # flags to keep data coherent when enable state changes
        self.lastData_invalidate = False
        self.readPending_invalidate = False

    def setEnable_asDriver(self, en, sim):
        self._enabled = en
        self.driver.setEnable(en, sim)
        self.intf.wait.write(not en)
        self.lastData_invalidate = not en

    def setEnable_asMonitor(self, en, sim):
        lastEn = self._enabled
        self._enabled = en
        self.monitor.setEnable(en, sim)
        self.intf.en.write(en)
        self.readPending_invalidate = not en
        if not lastEn:
            self.dataReader.setEnable(en, sim)

    def driver_init(self, sim):
        self.intf.wait.write(not self._enabled)
        return
        yield

    def monitor_init(self, sim):
        self.intf.en.write(self._enabled)
        return
        yield

    def dataReader(self, sim):
        if self.readPending:
            yield sim.waitOnCombUpdate()
            d = self.intf.data.read()
            self.data.append(d)

            if self.readPending_invalidate:
                self.readPending = False

    def getMonitors(self):
        self.dataReader = OnRisingCallbackLoop(self.clk,
                                               self.dataReader,
                                               self.getEnable)
        return ([self.monitor_init] +
                super(FifoReaderAgent, self).getMonitors() +
                [self.dataReader])

    def monitor(self, sim):
        intf = self.intf

        if self.notReset(sim):
            # speculative en set
            yield sim.waitOnCombUpdate()
            wait = intf.wait.read()
            assert wait.vldMask, (sim.now, intf, "wait signal in invalid state")
            rd = not wait.val
            intf.en.write(rd)

        else:
            intf.en.write(0)
            rd = False

        self.readPending = rd

    def getDrivers(self):
        self.dataWriter = OnRisingCallbackLoop(self.clk,
                                               self.dataWriter,
                                               self.getEnable)
        return ([self.driver_init] +
                super(FifoReaderAgent, self).getDrivers() +
                [self.dataWriter])

    def dataWriter(self, sim):
        # delay data litle bit to have nicer wave
        # otherwise wirte happens before next clk period
        # and it means in 0 time and we will not be able to see it in wave
        yield Timer(DEFAULT_CLOCK / 10)
        self.intf.data.write(self.lastData)
        if self.lastData_invalidate:
            self.lastData = None

    def driver(self, sim):
        # now we are before clock event
        # * set wait signal
        # * set last data (done in separate process)
        # * if en == 1, pop next data for next clk
        intf = self.intf
        rst_n = self.notReset(sim)
        # speculative write
        if rst_n and self.data:
            wait = 0
        else:
            wait = 1

        intf.wait.write(wait)

        if rst_n:
            yield sim.waitOnCombUpdate()
            # wait for potential update of en
            yield sim.waitOnCombUpdate()
            # check if write can be performed and if it possible do real write

            en = intf.en.read()
            try:
                en = int(en)
            except ValueError:
                raise AssertionError(sim.now, intf, "en signal in invalid state")

            if en:
                assert self.data, (sim.now, intf, "underflow")
                self.lastData = self.data.popleft()


class FifoWriterAgent(SyncAgentBase):
    """
    Simulation agent for FifoWriter interface
    """

    def __init__(self, intf, allowNoReset=False):
        super(FifoWriterAgent, self).__init__(intf, allowNoReset=allowNoReset)
        self.data = deque()

    def driver_init(self, sim):
        self.intf.en.write(self._enabled)
        return
        yield

    def monitor_init(self, sim):
        self.intf.wait.write(not self._enabled)
        return
        yield

    def setEnable_asDriver(self, en, sim):
        SyncAgentBase.setEnable_asDriver(self, en, sim)
        self.intf.en.write(en)

    def setEnable_asMonitor(self, en, sim):
        SyncAgentBase.setEnable_asMonitor(self, en, sim)
        self.intf.wait.write(not en)

    def monitor(self, sim):
        # set wait signal
        # if en == 1 take data
        intf = self.intf
        intf.wait.write(0)

        yield sim.waitOnCombUpdate()
        # wait for potential update of en
        yield sim.waitOnCombUpdate()

        en = intf.en.read()
        try:
            en = int(en)
        except ValueError:
            raise AssertionError(sim.now, intf, "en signal in invalid state")

        if en:
            yield Timer(DEFAULT_CLOCK / 10)
            self.data.append(intf.data.read())

    def driver(self, sim):
        # if wait == 0 set en=1 and set data
        intf = self.intf

        if self.notReset(sim) and self.data:
            yield sim.waitOnCombUpdate()

            wait = intf.wait.read()
            assert wait.vldMask, (sim.now, intf, "wait signal in invalid state")
            if not wait.val:
                d = self.data.popleft()
                intf.data.write(d)
                intf.en.write(1)
                return

        intf.data.write(None)
        intf.en.write(0)

    def getDrivers(self):
        return SyncAgentBase.getDrivers(self) + [self.driver_init]

    def getMonitors(self):
        return SyncAgentBase.getMonitors(self) + [self.monitor_init]
