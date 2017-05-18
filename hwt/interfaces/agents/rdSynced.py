from hwt.simulator.agentBase import SyncAgentBase
from hwt.hdlObjects.constants import NOP


class RdSyncedAgent(SyncAgentBase):
    """
    Simulation/verification agent for RdSynced interface
    """
    def __init__(self, intf, clk=None, rstn=None):
        super().__init__(intf, clk=clk, rstn=rstn, allowNoReset=True)
        self.actualData = NOP
        self.data = []
        self._rd = intf.rd

    def monitor(self, s):
        """Collect data from interface"""
        intf = self.intf

        if self.notReset(s) and self.enable:
            s.w(1, intf.rd)

            yield s.updateComplete

            d = self.doRead(s)
            self.data.append(d)
        else:
            s.w(0, intf.rd)

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

        en = s.r(self.rst_n).val and self.enable
        if not (en and do):
            return

        yield s.updateComplete

        rd = s.r(self._rd)
        if en:
            assert rd.vldMask, "%r: ready signal for interface %r is in invalid state, this would cause desynchronization" % (s.now, self.intf)
        if rd.val:
            if self._debugOutput is not None:
                self._debugOutput.write("%s, wrote, %d: %r\n" % (
                                           self.intf._getFullName(), s.now, self.actualData))
            if self.data:
                self.actualData = self.data.pop(0)
            else:
                self.actualData = NOP
