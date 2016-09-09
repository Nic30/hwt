from hdl_toolkit.simulator.shortcuts import onRisingEdge
from hdl_toolkit.synthesizer.interfaceLevel.mainBases import UnitBase

class AgentBase():
    def __init__(self, intf):
        self.intf = intf
        self.enable = True
    
    def getDrivers(self):
        return [self.driver]
    
    def getMonitors(self):
        return [self.monitor]

    def driver(self, s):
        raise NotImplementedError()
    
    def monitor(self, s):
        raise NotImplementedError()

   
class SyncAgentBase(AgentBase):
    def getRst_n(self, parent, allowNoReset):
        while True:
            try:
                return parent.rst_n 
            except AttributeError:
                pass
            
            try:
                return ~parent.rst 
            except AttributeError:
                pass
            
            if isinstance(parent, UnitBase):
                break
            else:
                parent = parent._parent
        
        if allowNoReset:
            return None
        else:
            raise Exception("Can not find reset on unit %s" % (repr(parent)))
        
    
    def notReset(self, s):
        if self.rst_n is None:
            return True
        else:
            return s.r(self.rst_n).val
    
    def _getClk(self):
        p = self.intf._parent
        while True:
            try:
                return p.clk
            except AttributeError:
                if isinstance(p, UnitBase):
                    raise Exception("Can not find clk")
                p = p._parent
        return None
    
    def __init__(self, intf, clk=None, rstn=None, allowNoReset=False):
        super().__init__(intf)
        
        # resolve clk and rstn
        if clk is None:
            self.clk = self._getClk()
        else:
            self.clk = clk
            
        if rstn is None:
            self.rst_n = self.getRst_n(intf._parent, allowNoReset=allowNoReset)
        else:
            self.rst_n = rstn

        
        self.monitor = onRisingEdge(self.clk, self.monitor)
        self.driver = onRisingEdge(self.clk, self.driver)