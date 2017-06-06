from hwt.hdlObjects.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase


class RdSyncedAgent(SyncAgentBase):
    """
    Simulation/verification agent for RdSynced interface
    """
    def __init__(self, intf, allowNoReset=True):
        super().__init__(intf, allowNoReset=allowNoReset)
        self.actualData = NOP
        self.data = []
        self._rd = intf.rd

    def monitor(self, s):
        """Collect data from interface"""
        intf = self.intf

        if self.notReset(s) and self.enable:
            s.write(1, intf.rd)

            yield s.updateComplete

            d = self.doRead(s)
            self.data.append(d)
        else:
            s.write(0, intf.rd)

    def doRead(self, s):
        """extract data from interface"""
        return s.read(self.intf.data)

    def doWrite(self, s, data):
        """write data to interface"""
        s.write(data, self.intf.data)

    def driver(self, s):
        """Push data to interface"""
        r = s.read
        if self.actualData is NOP and self.data:
            self.actualData = self.data.pop(0)

        do = self.actualData is not NOP

        if do:
            self.doWrite(s, self.actualData)
        else:
            self.doWrite(s, None)

        en = r(self.rst_n).val and self.enable
        if not (en and do):
            return

        yield s.updateComplete

        rd = r(self._rd)
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
