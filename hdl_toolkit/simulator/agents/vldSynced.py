from hdl_toolkit.simulator.agents.agentBase import AgentBase
from hdl_toolkit.simulator.shortcuts import afterRisingEdge


class VldSyncedAgent(AgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        self.intf = intf
        
        p = intf._parent
        if clk is None:
            self.clk = p.clk
        else:
            self.clk = clk
        if rstn is None:
            self.rst_n = p.rst_n 
        else:
            self.rst_n = rstn
            
        self.wait = False
        self.data = []
        
        self.monitor = afterRisingEdge(self.clk)(self.monitor)
        self.driver = afterRisingEdge(self.clk)(self.driver)
        
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