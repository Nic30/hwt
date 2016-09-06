from hdl_toolkit.simulator.agents.agentBase import SyncAgentBase


class VldSyncedAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None, allowNoReset=False):
        super(VldSyncedAgent, self).__init__(intf, clk=clk, rstn=rstn, allowNoReset=allowNoReset)
        self.data = []
    
    def doRead(self, s):
        return s.read(self.intf)
        
    def doWrite(self, s, data):
        s.w(data, self.intf.data)
        
    def monitor(self, s):
        intf = self.intf
        if self.enable and s.r(self.rst_n).val and s.r(intf.vld).val:
            self.data.push(self.doRead(s))
            
    def driver(self, s):
        intf = self.intf
        
        if self.enable and self.data and s.r(self.rst_n).val :
            d = self.data.pop(0)
            self.doWrite(s, d)
            s.w(1, intf.vld)
        else:
            self.doWrite(s, None)
            s.w(0, intf.vld)