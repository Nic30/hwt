from hdl_toolkit.simulator.agents.agentBase import SyncAgentBase

class HandshakedAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=None, rstn=None)
        self.actualData = None
        self.data = []
        
    def monitor(self, s):
        """
        Collect data
        """
        intf = self.intf
        
        if s.r(self.rst_n).val and self.enable:
            vld = s.r(intf.vld).val
            if vld:
                d = self.doRead(s)
                self.data.append(d)
            s.w(1, intf.rd)
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
        if s.r(self.rst_n).val and self.actualData is not None and self.enable:
            s.w(1, intf.vld)
        else:
            s.w(0, intf.vld)
        
        yield s.updateComplete
        
        rd = s.r(intf.rd).val
        if rd:
            if self.data:
                self.actualData = self.data.pop(0)
            else:
                self.actualData = None

class HandshakeSyncAgent(HandshakedAgent):
    def doWrite(self, s, data):
        pass
    
    def doRead(self, s):
        raise NotImplementedError()    