from hdl_toolkit.simulator.agents.agentBase import SyncAgentBase


class RdSyncedAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=None, rstn=None, allowNoReset=True)
        self.actualData = None
        
    def monitor(self, s):
        """
        Collect data
        """
        intf = self.intf
        
        if self.notReset(s) and self.enable:
            s.w(1, intf.rd)
            
            while s.applyValuesPlaned:
                yield s.wait(0)
            d = self.doRead(s)
            self.data.append(d)
        else:
            s.w(0, intf.rd)
    
    def doRead(self, s):
        return s.read(self.intf.data)
        
    def doWrite(self, s, data):
        if data is None:
            s.w(0, self.intf.data)
        else:
            s.w(data, self.intf.data)
        
    def driver(self, s):
        intf = self.intf
        
        if self.actualData is None and self.data:
            self.actualData = self.data.pop(0)
        
        self.doWrite(s, self.actualData)
        if self.notReset(s) and self.actualData is not None and self.enable:
            s.w(1, intf.vld)
            while s.applyValuesPlaned:
                yield s.wait(0)
                    
            d = self.doRead(s)
            self.data.append(d)
        else:
            s.w(0, intf.vld)



    