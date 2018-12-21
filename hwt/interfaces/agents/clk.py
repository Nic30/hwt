from hwt.hdl.constants import CLK_PERIOD
from hwt.simulator.agentBase import AgentBase
from pycocotb.process_utils import CallbackLoop
from pycocotb.triggers import WriteOnly, Timer, ReadOnly

DEFAULT_CLOCK = CLK_PERIOD


class OscilatorAgent(AgentBase):
    """
    Simulation agent for :class:`hwt.interfaces.std.Clk` interface

    * In driver mode oscillates at frequency specified by period

    * In monitor driver captures tuples (time, nextVal) for each change
        on signal (nextVal is 1/0/None)

    :ivar period: period of signal to generate
    :ivar initWait: time to wait before starting oscillation
    """

    def __init__(self, intf, period=DEFAULT_CLOCK):
        super(OscilatorAgent, self).__init__(intf)
        self.period = period
        self.initWait = 0
        self.intf = self.intf._sigInside
        self.monitor = CallbackLoop(self.intf, self.monitor, self.getEnable)

    def driver(self, sim):
        sig = self.intf

        sig.write(0)
        halfPeriod = self.period // 2
        yield Timer(self.initWait)

        while True:

            yield Timer(halfPeriod)
            yield WriteOnly
            sig.write(1)

            yield Timer(halfPeriod)
            yield WriteOnly
            sig.write(0)

    def getMonitors(self):
        self.last = (-1, None)
        self.data = []

        return [self.monitor]

    def monitor(self, sim):
        yield ReadOnly
        v = self.intf.read()
        try:
            v = int(v)
        except ValueError:
            v = None

        now = sim.now
        last = self.last

        _next = (now, v)
        if last[0] == now:
            if last[1] is not v:
                # update last value
                last = (now, v)
                self.last = last
                if self.data:
                    self.data[-1] = last
                else:
                    self.data.append(last)
            else:
                return
        else:
            self.data.append(_next)

        self.last = _next
