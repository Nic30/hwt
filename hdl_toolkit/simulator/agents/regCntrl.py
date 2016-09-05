

from hdl_toolkit.simulator.agents.agentBase import SyncAgentBase


class RegCntrlAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=None, rstn=None, allowNoReset=True)
        self.requests = []
        self.rx = []
        self.tx = []
        self.readPending = False
        
    def monitor(self, s):
        """
        Collect data
        """
        raise NotImplementedError()
    
    def doRead(self, s):
        return s.read(self.intf.din)
        
    def doWrite(self, s, data):
        if data is None:
            s.w(0, self.intf.dout.data)
        else:
            s.w(data, self.intf.dout.data)
        
    def driver(self, s):
        intf = self.intf
        
        if self.enable and self.tx:
            data = self.tx.pop(0)
            self.doWrite(s, data)
            s.w(1, intf.dout.vld)
        else:
            self.doWrite(s, None)
            s.w(0, intf.dout.vld)
        
        self.rx.append(self.doRead(s))