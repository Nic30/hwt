

from hdl_toolkit.simulator.agents.agentBase import SyncAgentBase


class RegCntrlAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=None, rstn=None, allowNoReset=True)
        self.actualData = None
        
    def monitor(self, s):
        """
        Collect data
        """
        raise NotImplementedError()
    
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
        raise NotImplementedError()
