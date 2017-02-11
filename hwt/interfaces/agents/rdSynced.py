from hwt.simulator.agentBase import SyncAgentBase


class RdSyncedAgent(SyncAgentBase):
    """
    Simulation/verification agent for RdSynced interface
    """
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=clk, rstn=rstn, allowNoReset=True)
        self.actualData = None
        
    def monitor(self, s):
        """Collect data from interface"""
        intf = self.intf
        
        if self.notReset(s) and self.enable:
            s.w(1, intf.rd)
            
            yield s.updateComplete
            
            d = self.doRead(s)
            self.data.append(d)
        else:
            s.w(0, intf.rd)
    
    def doRead(self, s):
        """extract data from interface"""
        return s.read(self.intf.data)
        
    def doWrite(self, s, data):
        """write data to interface"""
        s.w(data, self.intf.data)
        
    def driver(self, s):
        """Push data to interface"""
        intf = self.intf
        
        if self.actualData is None and self.data:
            self.actualData = self.data.pop(0)
        
        self.doWrite(s, self.actualData)
        if self.notReset(s) and self.actualData is not None and self.enable:
            s.w(1, intf.vld)
            yield s.updateComplete
                    
            d = self.doRead(s)
            self.data.append(d)
        else:
            s.w(0, intf.vld)



    