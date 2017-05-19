from hwt.hdlObjects.constants import Time
from hwt.simulator.agentBase import AgentBase


class OscilatorAgent(AgentBase):
    def __init__(self, intf, period=10 * Time.ns):
        super(OscilatorAgent, self).__init__(intf)
        self.period = period
        self.initWait = 0
        
    def driver(self, s):
        sig = self.intf
        s.write(False, sig)
        halfPeriod = self.period / 2
        yield s.wait(self.initWait)

        while True:
            yield s.wait(halfPeriod)
            s.write(1, sig)
            yield s.wait(halfPeriod)
            s.write(0, sig)
