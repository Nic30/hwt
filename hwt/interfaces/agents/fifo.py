from collections import deque

from hwt.simulator.agentBase import SyncAgentBase
from hwt.simulator.shortcuts import OnRisingCallbackLoop
from hwt.interfaces.agents.signal import DEFAULT_CLOCK


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
        sim.write(not en, self.intf.wait)
        self.lastData_invalidate = not en

    def setEnable_asMonitor(self, en, sim):
        lastEn = self._enabled
        self._enabled = en
        self.monitor.setEnable(en, sim)
        sim.write(en, self.intf.en)
        self.readPending_invalidate = not en
        if not lastEn:
            self.dataReader.setEnable(en, sim)

    def driver_init(self, sim):
        sim.write(not self._enabled, self.intf.wait)
        return
        yield

    def monitor_init(self, sim):
        sim.write(self._enabled, self.intf.en)
        return
        yield

    def dataReader(self, sim):
        if self.readPending:
            yield sim.waitOnCombUpdate()
            d = sim.read(self.intf.data)
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
        r = sim.read
            
        if self.notReset(sim):
            # speculative en set
            yield sim.waitOnCombUpdate()
            wait = r(intf.wait)
            assert wait.vldMask, (intf, sim.now)
            rd = not wait.val
            sim.write(rd, intf.en)

        else:
            sim.write(0, intf.en)
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
        yield sim.wait(DEFAULT_CLOCK / 10)
        sim.write(self.lastData, self.intf.data)
        if self.lastData_invalidate:
            self.lastData = None
        
    def driver(self, sim):
        # now we are before clock event
        # * set wait signal
        # * set last data (done in separate process)
        # * if en == 1, pop next data for next clk
        intf = self.intf
        w = sim.write
        rst_n = self.notReset(sim)
        # speculative write
        if rst_n and self.data:
            wait = 0
        else:
            wait = 1

        w(wait, intf.wait)

        if rst_n:
            yield sim.waitOnCombUpdate()
            # wait for potential update of en
            yield sim.waitOnCombUpdate()
            # check if write can be performed and if it possible do real write
    
            en = sim.read(intf.en)
            assert en.vldMask, (intf, sim.now)
            if en.val:
                assert self.data, ("underflow", intf, sim.now)
                self.lastData = self.data.popleft()



class FifoWriterAgent(SyncAgentBase):
    """
    Simulation agent for FifoWriter interface
    """
    def __init__(self, intf, allowNoReset=False):
        super(FifoWriterAgent, self).__init__(intf, allowNoReset=allowNoReset)
        self.data = deque()

    def driver_init(self, sim):
        sim.write(self._enabled, self.intf.en)
        return
        yield

    def monitor_init(self, sim):
        sim.write(not self._enabled, self.intf.wait)
        return
        yield

    def setEnable_asDriver(self, en, sim):
        SyncAgentBase.setEnable_asDriver(self, en, sim)
        sim.write(en, self.intf.en)

    def setEnable_asMonitor(self, en, sim):
        SyncAgentBase.setEnable_asMonitor(self, en, sim)
        sim.write(not en, self.intf.wait)

    def monitor(self, sim):
        # set wait signal
        # if en == 1 take data
        intf = self.intf
        sim.write(0, intf.wait)

        yield sim.waitOnCombUpdate()
        # wait for potential update of en
        yield sim.waitOnCombUpdate()

        en = sim.read(intf.en)
        assert en.vldMask
        if en.val:
            yield sim.wait(DEFAULT_CLOCK / 10)
            self.data.append(sim.read(intf.data))

    def driver(self, sim):
        # if wait == 0 set en=1 and set data 
        intf = self.intf
        w = sim.write

        if self.notReset(sim) and self.data:
            yield sim.waitOnCombUpdate()

            wait = sim.read(intf.wait)
            assert wait.vldMask
            if not wait.val:
                d = self.data.popleft()
                w(d, intf.data)
                w(1, intf.en)
                return

        w(None, intf.data)
        w(0, intf.en)

    def getDrivers(self):
        return SyncAgentBase.getDrivers(self) + [self.driver_init]

    def getMonitors(self):
        return SyncAgentBase.getMonitors(self) + [self.monitor_init]
