from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
ns = HdlSimulator.ns

class SignalAgent(AgentBase):
    READER_DELAY = 0.001 # random small value
    def __init__(self, intf, delay=10*ns):
        self.delay = delay
        self.intf = intf
        self.data = []
    
    def doRead(self, s):
        return s.read(self.intf)
        
    def doWrite(self, s, data):
        s.w(data, self.intf)    
        
    def driver(self, s):
        while True:
            if self.data:
                self.doWrite(s, self.data.pop(0))
            yield s.wait(self.delay)
    
    def monitor(self, s):
        yield s.wait(self.READER_DELAY)
        while True:
            while s.applyValuesPlaned:
                yield s.wait(0)
            d = self.doRead(s)
            self.data.append(d)
            yield s.wait(self.delay)
    