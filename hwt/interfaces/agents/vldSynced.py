from collections import deque

from hwt.hdl.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase


class VldSyncedAgent(SyncAgentBase):

    def __init__(self, intf, allowNoReset=False):
        super(VldSyncedAgent, self).__init__(
            intf,
            allowNoReset=allowNoReset)
        self.data = deque()

    def doRead(self, sim):
        return self.intf.data.read()

    def doWrite(self, sim, data):
        self.intf.data.write(data)

    def doReadVld(self):
        return self.intf.vld.read()

    def doWriteVld(self, val):
        return self.intf.vld.write(val)

    def setEnable_asDriver(self, en, sim):
        super(VldSyncedAgent, self).setEnable_asDriver(en, sim)
        if not en:
            self.wrVld(0)
            self._lastVld = 0

    def monitor(self, sim):
        yield WaitCombRead()
        if self.notReset():
            intf = self.intf
            vld = self.doReadVld()
            vld = int(vld)
            if vld:
                d = self.doRead()

                if self._debugOutput is not None:
                    self._debugOutput.write("%s, read, %d: %r\n" % (
                        intf._getFullName(),
                        sim.now, d))
                self.data.append(d)

    def driver(self, sim):
        yield WaitCombRead()
        if self.data and self.notReset():
            yield WaitWriteOnly()
            d = self.data.popleft()
            if d is NOP:
                self.doWrite(sim, None)
                self.doWriteVld(0)
            else:
                self.doWrite(sim, d)
                self.doWriteVld(1)
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, wrote, %d: %r\n" % (
                        self.intf._getFullName(),
                        sim.now, self.actualData))

        else:
            self.doWrite(sim, None)
            self.doWriteVld(0)
