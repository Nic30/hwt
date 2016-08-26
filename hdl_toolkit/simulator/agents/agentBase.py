from hdl_toolkit.simulator.shortcuts import onRisingEdge

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
    def getRst_n(self, unit, allowNoReset):
        try:
            return unit.rst_n 
        except AttributeError:
            pass
        
        try:
            return ~unit.rst 
        except AttributeError:
            pass
        
        if allowNoReset:
            return None
        else:
            raise Exception("Can not find reset on unit %s" % (repr(unit)))
        
    
    def notReset(self, s):
        if self.rst_n is None:
            return True
        else:
            s.r(self.rst_n).val
        
    def __init__(self, intf, clk=None, rstn=None, allowNoReset=False):
        super().__init__(intf)
        
        # resolve clk and rstn
        p = intf._parent
        if clk is None:
            self.clk = p.clk
        else:
            self.clk = clk
            
        if rstn is None:
            self.rst_n = self.getRst_n(p, allowNoReset=allowNoReset)
        else:
            self.rst_n = rstn

        
        self.monitor = onRisingEdge(self.clk, self.monitor)
        self.driver = onRisingEdge(self.clk, self.driver)