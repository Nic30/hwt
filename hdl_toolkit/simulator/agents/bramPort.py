from hdl_toolkit.hdlObjects.specialValues import READ, WRITE
from hdl_toolkit.simulator.agents.agentBase import SyncAgentBase
from hdl_toolkit.simulator.shortcuts import oscilate, afterRisingEdge


class BramPort_withoutClkAgent(SyncAgentBase):
    """
    @ivar requests: list of tuples (request type, address) - used for driver
    @ivar data:     list of data in memory, used for monitor
    """
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=clk, rstn=rstn, allowNoReset=True)
        
        self.requests = []
        self.readPending = False
        self.readed = []
        
        self.monitor = afterRisingEdge(self.clk, self.monitor)
        self.driver = afterRisingEdge(self.clk, self.driver)

    def doReq(self, s, req):
        rw = req[0]
        addr = req[1]
        
        if rw == READ:
            rw = 0
            wdata = None
            self.readPending = True
            
        elif rw == WRITE:
            wdata = req[2] 
            rw = 1
        else:
            raise NotImplementedError(rw)
        
        intf = self.intf
        s.w(rw, intf.we)
        s.w(addr, intf.addr)
        s.w(wdata, intf.din)
    
    def onReadReq(self, s, addr):
        """
        on readReqRecieved
        """
        raise NotImplementedError()

    def onWriteReq(self, s, addr, data):
        raise NotImplementedError()
    
    def monitor(self, s):
        intf = self.intf
        if self.enable and s.read(intf.en).val:
            we = self.read(intf.we)
            addr = self.read(intf.addr)
            if we.val:
                data = self.read(intf.din)
                self.onWriteReq(s, addr, data)
            else:
                self.onReadReq(s, addr)

    def driver(self, s):
        intf = self.intf
        
        if self.requests and self.enable:
            req = self.requests.pop(0)
            self.doReq(s, req)
            
            s.w(1, intf.en)
        else:
            s.w(0, intf.en)
        
        if self.readPending:
            d = s.r(intf.dout)
            self.readed.append(d)
            self.readPending = False
    


class BramPortAgent(BramPort_withoutClkAgent):
    def __init__(self, intf, clk=None, rstn=None):
        if clk is None:
            clk = intf.clk
        super().__init__(intf, clk=clk, rstn=rstn)
        
    def getSubDrivers(self):
        yield oscilate(self.intf.clk)
