from collections import deque

from hwt.hdl.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase


class VldSyncedAgent(SyncAgentBase):
    def __init__(self, intf, allowNoReset=False):
        super(VldSyncedAgent, self).__init__(intf, allowNoReset=allowNoReset)
        self.data = deque()

    def doRead(self, s):
        return s.read(self.intf.data)

    def doWrite(self, s, data):
        s.write(data, self.intf.data)

    def monitor(self, s):
        intf = self.intf
        yield s.updateComplete
        if self.enable and self.notReset(s):
            vld = s.read(intf.vld)
            assert vld.vldMask, "valid signal for interface %r is in invalid state, this would cause desynchronization in %d" % (self.intf, s.now)
            if vld.val:
                d = self.doRead(s)

                if self._debugOutput is not None:
                    self._debugOutput.write("%s, read, %d: %r\n" % (
                                              self.intf._getFullName(), s.now, d))
                self.data.append(d)

    def driver(self, s):
        intf = self.intf

        if self.enable and self.data and self.notReset(s):
            d = self.data.popleft()
            if d is NOP:
                self.doWrite(s, None)
                s.write(0, intf.vld)
            else:
                self.doWrite(s, d)
                s.write(1, intf.vld)
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, wrote, %d: %r\n" % (
                                                self.intf._getFullName(), s.now, self.actualData))

        else:
            self.doWrite(s, None)
            s.write(0, intf.vld)
