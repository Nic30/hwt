from collections import deque

from hwt.simulator.agentBase import SyncAgentBase
from hwt.synthesizer.exceptions import IntfLvlConfErr
from pycocotb.agents.base import AgentBase
from pycocotb.agents.clk import DEFAULT_CLOCK
from pycocotb.triggers import Timer


class SignalAgent(SyncAgentBase):
    """
    Agent for signal interface, it can use clock and reset interface
    for synchronization or can be synchronized by delay

    :attention: clock synchronization has higher priority
    """

    def __init__(self, intf, delay=None):
        AgentBase.__init__(self, intf)
        self.delay = delay
        self.initDelay = 0

        # resolve clk and rstn
        try:
            self.clk = self.intf._getAssociatedClk()
        except IntfLvlConfErr:
            self.clk = None

        self._discoverReset(True)
        self.data = deque()

        self.initPending = True

        if self.clk is None:
            if self.delay is None:
                self.delay = DEFAULT_CLOCK
            self.monitor = self.monitorWithTimer
            self.driver = self.driverWithTimer
        else:
            if self.initDelay:
                raise NotImplementedError("initDelay only without clock")
            c = self.SELECTED_EDGE_CALLBACK
            self.monitor = c(self.clk, self.monitorWithClk, self.getEnable)
            self.driver = c(self.clk, self.driverWithClk, self.getEnable)

    def getDrivers(self):
        d = SyncAgentBase.getDrivers(self)
        return [self.driverInit] + d

    def driverInit(self, sim):
        yield sim.waitWriteOnly()
        try:
            d = self.data[0]
        except IndexError:
            d = None

        self.doWrite(sim, d)

        return
        yield

    def doRead(self, s):
        return self.intf.read()

    def doWrite(self, s, data):
        self.intf.write(data)

    def driverWithClk(self, sim):
        # if clock is specified this function is periodically called every
        # clk tick, if agent is enabled
        yield sim.waitReadOnly()
        if self.data and self.notReset(sim):
            yield sim.waitWriteOnly()
            d = self.data.popleft()
            self.doWrite(sim, d)

    def driverWithTimer(self, sim):
        if self.initPending:
            if self.initDelay:
                yield Timer(self.initDelay)
            self.initPending = False
        # if clock is specified this function is periodically called every
        # clk tick
        while True:
            yield sim.waitReadOnly()
            if self._enabled and self.data and self.notReset(sim):
                yield sim.waitWriteOnly()
                d = self.data.popleft()
                self.doWrite(sim, d)

            yield Timer(self.delay)

    def monitorWithTimer(self, sim):
        if self.initPending and self.initDelay:
            yield Timer(self.initDelay)
            self.initPending = False
        # if there is no clk, we have to manage periodic call by our self
        while True:
            yield sim.waitReadOnly()
            if self._enabled and self.notReset(sim):
                d = self.doRead(sim)
                self.data.append(d)

            yield Timer(self.delay)

    def monitorWithClk(self, sim):
        # if clock is specified this function is periodically called every
        # clk tick, when agent is enabled
        yield sim.waitReadOnly()
        if self.notReset(sim):
            d = self.doRead(sim)
            self.data.append(d)
