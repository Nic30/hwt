from hwt.hdlObjects.constants import Time
from hwt.simulator.agentBase import AgentBase
from hwt.simulator.shortcuts import CallbackLoop


class OscilatorAgent(AgentBase):
    """
    Simulation agent for :class:`hwt.interfaces.std.Clk` interface
    
    * In driver mode oscillates at frequency specified by period
    
    * In monitor driver captures tuples (time, nextVal) for each change on signal (nextVal is 1/0/None)
    
    :ivar period: period of signal to generate
    :ivar initWait: time to wait before starting oscillation 
    """
    def __init__(self, intf, period=10 * Time.ns):
        super(OscilatorAgent, self).__init__(intf)
        self.period = period
        self.initWait = 0
        
    def driver(self, s):
        sig = self.intf
        s.write(0, sig)
        halfPeriod = self.period / 2
        yield s.wait(self.initWait)

        while True:
            yield s.wait(halfPeriod)
            s.write(1, sig)
            yield s.wait(halfPeriod)
            s.write(0, sig)

    def getMonitors(self):
        self.last = (-1, None)
        self.data = []

        c = CallbackLoop(self.intf, lambda s, intf: True, self.monitor)
        return [c.initProcess, ]

    def monitor(self, s):
        yield s.updateComplete
        v = s.read(self.intf)
        if not v.vldMask:
            v = None
        else:
            v = v.val

        now = s.now
        last = self.last

        next = (now, v)
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
            self.data.append(next)
        
        self.last = next
            
