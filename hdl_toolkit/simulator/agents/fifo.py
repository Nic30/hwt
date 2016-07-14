from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.shortcuts import afterRisingEdge

class FifoReaderAgent(AgentBase):
    def __init__(self, intf, getClkFn=lambda u:u.clk, getRstnFn=lambda u: u.rst_n):
        self.intf = intf
        self.clk = getClkFn(intf._parent)
        self.rst_n = getRstnFn(intf._parent) 
        self.wait = False
        self.data = []
        
        self.monitor = afterRisingEdge(lambda : self.clk)(self.monitor)
        self.driver = afterRisingEdge(lambda : self.clk)(self.driver)
        
    def monitor(self, s):
        intf = self.intf
        
        if s.r(self.rst_n).val and not self.wait:
            rd = not s.r(intf.wait).val
            if rd:
                d = s.read(intf.data)
                self.data.append(d)
            s.w(rd, intf.en)
        else:
            s.w(0, intf.en)
            
    def driver(self, s):
        raise NotImplementedError()

class FifoWriterAgent(AgentBase):
    def __init__(self, intf, getClkFn=lambda u:u.clk, getRstnFn=lambda u: u.rst_n):
        self.intf = intf
        self.clk = getClkFn(intf._parent)
        self.rst_n = getRstnFn(intf._parent) 
        self.wait = False
        self.data = []
        
        self.monitor = afterRisingEdge(lambda : self.clk)(self.monitor)
        self.driver = afterRisingEdge(lambda : self.clk)(self.driver)
        
    def monitor(self, s):
        raise NotImplementedError()
            
    def driver(self, s):
        intf = self.intf
        
        if s.r(self.rst_n).val and not s.r(intf.wait).val and self.data:
            print("next %f" % s.env.now)
            s.w(self.data.pop(0), intf.data)
            s.w(1, intf.en)
        else:
            print("wait %f" % s.env.now)
            s.w(0, intf.data)
            s.w(0, intf.en)