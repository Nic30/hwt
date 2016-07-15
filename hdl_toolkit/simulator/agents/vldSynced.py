from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.shortcuts import afterRisingEdge


class VldSyncedAgent(AgentBase):
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
        
        if s.r(self.rst_n).val and self.data:
            s.w(self.data.pop(0), intf.data)
            s.w(1, intf.vld)
        else:
            s.w(0, intf.data)
            s.w(0, intf.vld)