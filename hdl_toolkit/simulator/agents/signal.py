from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.hdlObjects.specialValues import Time

class SignalAgent(AgentBase):
    def __init__(self, intf, delay=10 * Time.ns):
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
        while True:
            yield s.updateComplete
            d = self.doRead(s)
            self.data.append(d)
            yield s.wait(self.delay)
    
