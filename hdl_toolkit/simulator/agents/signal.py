from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.hdlSimulator import HdlSimulator
ns = HdlSimulator.ns

class SignalAgent(AgentBase):
    def __init__(self, intf, delay=10*ns):
        self.delay = delay
        self.intf = intf
        self.data = []
        
        
    def driver(self, s):
        while True:
            sig = self.intf
            if self.data:
                s.write(self.data.pop(0), sig)
            yield s.wait(self.delay)
    
    def monitor(self, s):
        while True:
            sig = self.intf
            self.data.append(s.read(sig))
            yield s.wait(self.delay)
    