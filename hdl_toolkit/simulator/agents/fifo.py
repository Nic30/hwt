from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.shortcuts import afterRisingEdge

class FifoReaderAgent(AgentBase):
    def __init__(self, unit, getInfFn, getClkFn=lambda u:u.clk, getRstnFn=lambda u: u.rst_n):
        self.getInfFn = getInfFn
        self.getRstnFn = getRstnFn
        self.readerWait = False
        self.data = []
        
        self.monitor = afterRisingEdge(getClkFn)(self.monitor)
        self.driver = afterRisingEdge(getClkFn)(self.driver)
        
    def monitor(self, s):
        intf = self.getInfFn(self.unit)
        rst_n = self.getRstnFn(self.unit)
        
        if s.r(rst_n).val:
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
    def __init__(self, unit, getInfFn, getClkFn=lambda u: u.clk, getRstnFn=lambda u: u.rst_n):
        self.getInfFn = getInfFn
        self.getRstnFn = getRstnFn
        self.data = []
        
        self.monitor = afterRisingEdge(getClkFn)(self.monitor)
        self.driver = afterRisingEdge(getClkFn)(self.driver)
        
    def monitor(self, s):
        raise NotImplementedError()
            
    def driver(self, s):
        intf = self.getInfFn(self.unit)
        rst_n = self.getRstnFn(self.unit)
        
        if s.r(rst_n).val and self.data:
            s.w(self.data.pop(), intf.data)
            s.w(1, intf.en)
        else:
            s.w(0, intf.data)
            s.w(0, intf.en)