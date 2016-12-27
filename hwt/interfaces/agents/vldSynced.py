from hwt.simulator.agentBase import SyncAgentBase
from hwt.hdlObjects.constants import NOP


class VldSyncedAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None, allowNoReset=False):
        super(VldSyncedAgent, self).__init__(intf, clk=clk, rstn=rstn, allowNoReset=allowNoReset)
        self.data = []
    
    def doRead(self, s):
        return s.read(self.intf.data)
        
    def doWrite(self, s, data):
        s.w(data, self.intf.data)
        
    def monitor(self, s):
        intf = self.intf
        if self.enable and self.notReset(s) and s.r(intf.vld).val:
            self.data.append(self.doRead(s))
            
    def driver(self, s):
        intf = self.intf
        
        if self.enable and self.data and self.notReset(s):
            d = self.data.pop(0)
            if d is NOP:
                self.doWrite(s, None)
                s.w(0, intf.vld)
            else:
                self.doWrite(s, d)
                s.w(1, intf.vld)
        else:
            self.doWrite(s, None)
            s.w(0, intf.vld)