from hdl_toolkit.simulator.agentBase import SyncAgentBase
from hdl_toolkit.hdlObjects.specialValues import NOP


class HandshakedAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=None, rstn=None)
        self.actualData = NOP
        self.data = []
        # these signals are extracted like this to make 
        # agent more configurable
        self._rd = self.getRd()
        self._vld = self.getVld()
    
    def getRd(self):
        """get "ready" signal"""
        return self.intf.rd
    
    def getVld(self):
        """get "valid" signal"""
        return self.intf.vld
        
    def monitor(self, s):
        """
        Collect data
        """
        if s.r(self.rst_n).val and self.enable:
            s.w(1, self._rd)
            
            yield s.updateComplete
            vld = s.r(self._vld)
            if vld.val or not vld.vldMask:
                d = self.doRead(s)
                self.data.append(d)
        else:
            s.w(0, self._rd)
    
    def doRead(self, s):
        return s.read(self.intf.data)
        
    def doWrite(self, s, data):
        s.w(data, self.intf.data)
        
    def driver(self, s):
        if self.actualData is NOP and self.data:
            self.actualData = self.data.pop(0)
        
        do = self.actualData is not NOP
        
        if do:
            self.doWrite(s, self.actualData)
        else:
            self.doWrite(s, None)
            
        if s.r(self.rst_n).val and do and self.enable:
            s.w(1, self._vld)
        else:
            s.w(0, self._vld)
            return
        
        yield s.updateComplete
        
        rd = s.r(self._rd) 
        if rd.val or not rd.vldMask:
            if self.data:
                self.actualData = self.data.pop(0)
            else:
                self.actualData = NOP

class HandshakeSyncAgent(HandshakedAgent):
    def doWrite(self, s, data):
        pass
    
    def doRead(self, s):
        raise NotImplementedError()    
    
