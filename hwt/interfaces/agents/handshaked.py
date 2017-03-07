from hwt.simulator.agentBase import SyncAgentBase
from hwt.hdlObjects.constants import NOP


class HandshakedAgent(SyncAgentBase):
    """
    Simulation/verification agent for handshaked interface
    @attention: requires clk and rst/rstn signal
      (if you do not have any create simulation wrapper with it)
    """
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=clk, rstn=rstn)
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
        Collect data from interface
        """
        if s.r(self.rst_n).val and self.enable:
            s.w(1, self._rd)

            yield s.updateComplete
            vld = s.r(self._vld)
            if vld.val or not vld.vldMask:
                d = self.doRead(s)
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, read, %d: %r\n" % (
                                            self.intf._getFullName(), s.now, d))
                self.data.append(d)
        else:
            s.w(0, self._rd)

    def doRead(self, s):
        """extract data from interface"""
        return s.read(self.intf.data)

    def doWrite(self, s, data):
        """write data to interface"""
        s.w(data, self.intf.data)

    def driver(self, s):
        """Push data to interface"""
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
            if self._debugOutput is not None:
                self._debugOutput.write("%s, wrote, %d: %r\n" % (
                                           self.intf._getFullName(), s.now, self.actualData))
            if self.data:
                self.actualData = self.data.pop(0)
            else:
                self.actualData = NOP


class HandshakeSyncAgent(HandshakedAgent):
    """
    Simulation/verification agent for HandshakedSycn interface
    @attention: there is no data channel on this interface it is synchronization only
    """

    def doWrite(self, s, data):
        pass

    def doRead(self, s):
        raise NotImplementedError()
