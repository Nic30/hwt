from collections import deque

from hwt.hdl.constants import Time
from hwt.simulator.agentBase import AgentBase
from hwt.simulator.shortcuts import onRisingEdge
from hwt.synthesizer.exceptions import IntfLvlConfErr


DEFAULT_CLOCK = 10 * Time.ns


class SignalAgent(AgentBase):
    """
    Agent for signal interface, it can use clock and reset interface for synchronization
    or can be synchronized by delay

    :attention: clock synchronization has higher priority
    """
    def __init__(self, intf, delay=DEFAULT_CLOCK):
        self.delay = delay
        self.initDelay = 0
        self.intf = intf

        # resolve clk and rstn
        try:
            self.clk = self.intf._getAssociatedClk()
        except IntfLvlConfErr:
            self.clk = None

        try:
            self.rst = self.intf._getAssociatedRst()
            assert self.clk is not None
        except IntfLvlConfErr:
            self.rst = None

        self.data = deque()

        self.initPending = True

        if self.clk is not None:
            self.monitor = onRisingEdge(self.clk, self.monitor)
            self.driver = onRisingEdge(self.clk, self.driver)

    def doRead(self, s):
        return s.read(self.intf)

    def doWrite(self, s, data):
        s.write(data, self.intf)

    def driver(self, s):
        if self.initPending and self.initDelay:
            yield s.wait(self.initDelay)
            self.initPending = False

        if self.clk is None:
            # if clock is specified this function is periodically called every
            # clk tick
            while True:
                if self.data:
                    try:
                        d = self.data.popleft()
                    except AttributeError:
                        d = next(self.data)
                    self.doWrite(s, d)
                yield s.wait(self.delay)
        else:
            # if clock is specified this function is periodically called every
            # clk tick
            if self.data:
                try:
                    d = self.data.popleft()
                except AttributeError:
                    d = next(self.data)

                self.doWrite(s, d)

    def monitor(self, s):
        if self.clk is None:
            if self.initPending and self.initDelay:
                yield s.wait(self.initDelay)
                self.initPending = False
            # if there is no clk, we have to manage periodic call by our selfs
            while True:
                yield s.updateComplete
                d = self.doRead(s)
                self.data.append(d)
                yield s.wait(self.delay)
        else:
            # if clock is specified this function is periodically called every
            # clk tick
            yield s.updateComplete
            d = self.doRead(s)
            self.data.append(d)
