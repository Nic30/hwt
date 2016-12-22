from hwt.simulator.agentBase import SyncAgentBase


class FifoReaderAgent(SyncAgentBase):
    
    def __init__(self, intf, clk=None, rstn=None, allowNoReset=False):
        super(FifoReaderAgent, self).__init__(intf, clk, rstn, allowNoReset)
        self.data = []
        self.readPending = False
        
    def monitor(self, s):
        intf = self.intf
        if self.readPending:
            yield s.updateComplete
            d = s.read(intf.data)
            self.data.append(d)
            self.readPending = False
        if s.r(self.rst_n).val and self.enable:
            
            rd = not s.r(intf.wait).val
            s.w(rd, intf.en)
            
            if rd:
                self.readPending = True
            #    self.readPending
            #    yield s.updateComplete
            #    d = s.read(intf.data)
            #    self.data.append(d)
        else:
            s.w(0, intf.en)
            
    def driver(self, s):
        raise NotImplementedError()

class FifoWriterAgent(SyncAgentBase):
        
    def monitor(self, s):
        raise NotImplementedError()
            
    def driver(self, s):
        intf = self.intf
        
        if s.r(self.rst_n).val and not s.r(intf.wait).val \
           and self.data and self.enable:
            s.w(self.data.pop(0), intf.data)
            s.w(1, intf.en)
        else:
            s.w(None, intf.data)
            s.w(0, intf.en)
