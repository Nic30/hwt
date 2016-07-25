from hdl_toolkit.simulator.shortcuts import afterRisingEdge

class AgentBase():
    def __init__(self, intf):
        self.intf = intf
        self.enable = True
        self.data = []
    
    def getSubDrivers(self):
        return []
    
    def getSubMonitors(self):
        return []

    def driver(self, s):
        raise NotImplementedError()
    
    def monitor(self, s):
        raise NotImplementedError()
    
class SyncAgentBase(AgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf)
        
        # resolve clk and rstn
        p = intf._parent
        if clk is None:
            self.clk = p.clk
        else:
            self.clk = clk
        if rstn is None:
            self.rst_n = p.rst_n 
        else:
            self.rst_n = rstn

        
        self.monitor = afterRisingEdge(self.clk, self.monitor)
        self.driver = afterRisingEdge(self.clk, self.driver)