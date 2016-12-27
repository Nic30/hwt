from hwt.hdlObjects.constants import READ, WRITE
from hwt.simulator.agentBase import SyncAgentBase
from hwt.simulator.shortcuts import oscilate


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
        
        yield s.updateComplete
        if self.enable and s.read(intf.en).val:
            we = self.read(intf.we)
            addr = self.read(intf.addr)
            if we.val:
                data = self.read(intf.din)
                self.onWriteReq(s, addr, data)
            else:
                self.onReadReq(s, addr)

    def getDrivers(self):
        drivers = [self.driver]
        try:
            clk = self.intf.clk
        except AttributeError:
            return drivers
        drivers.append(oscilate(clk))
        return drivers
         
        
    def driver(self, s):
        intf = self.intf
        readPending = self.readPending
        if self.requests and self.enable:
            req = self.requests.pop(0)
            if req is None:
                s.w(0, intf.en)
                self.readPending = False
            else:    
                self.doReq(s, req)
                s.w(1, intf.en)
        else:
            s.w(0, intf.en)
            self.readPending = False
        
        if readPending:
            yield s.updateComplete
            d = s.r(intf.dout)
            self.readed.append(d)
    


class BramPortAgent(BramPort_withoutClkAgent):
    def __init__(self, intf, clk=None, rstn=None):
        if clk is None:
            clk = intf.clk
        super().__init__(intf, clk=clk, rstn=rstn)
        
    def getSubDrivers(self):
        yield oscilate(self.intf.clk)
