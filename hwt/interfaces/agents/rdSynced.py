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
        self._rd = self.getRd(intf)
    
    def getRd(self, intf):
        return intf.rd
    
    def isRd(self, readFn):
        return readFn(self._rd)

    def wrRd(self, writeFn, val):
        writeFn(val, self._rd)
    
    def monitor(self, s):
        """Collect data from interface"""
        if self.notReset(s) and self.enable:
            self.wrRd(s.write, 1)

            yield s.updateComplete

            d = self.doRead(s)
            self.data.append(d)
        else:
            self.wrRd(s.write, 0)

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

        en = self.notReset(s) and self.enable
        if not (en and do):
            return

        yield s.updateComplete

        rd = self.isRd(r)
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
