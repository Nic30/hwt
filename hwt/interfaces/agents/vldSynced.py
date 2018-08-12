from collections import deque

from hwt.hdl.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase


class VldSyncedAgent(SyncAgentBase):

    def __init__(self, intf, allowNoReset=False):
        super(VldSyncedAgent, self).__init__(intf,
                                             allowNoReset=allowNoReset)
        self.data = deque()

    def doRead(self, s):
        return s.read(self.intf.data)

    def doWrite(self, s, data):
        s.write(data, self.intf.data)

    def doReadVld(self, readFn):
        return readFn(self.intf.vld)

    def doWriteVld(self, writeFn, val):
        return writeFn(val, self.intf.vld)

    def setEnable_asDriver(self, en, sim):
        super(VldSyncedAgent, self).setEnable_asDriver(en, sim)
        if not en:
            self.wrVld(sim.write, 0)
            self._lastVld = 0

    def monitor(self, sim):
        yield sim.waitOnCombUpdate()
        if self.notReset(sim):
            intf = self.intf
            vld = self.doReadVld(sim.read)
            assert vld.vldMask, (
                ("valid signal for interface %r is in invalid state,"
                 " this would cause desynchronization in %d") % 
                (intf, sim.now))
            if vld.val:
                d = self.doRead(sim)

                if self._debugOutput is not None:
                    self._debugOutput.write("%s, read, %d: %r\n" % (
                        intf._getFullName(),
                        sim.now, d))
                self.data.append(d)

    def driver(self, sim):
        if self.data and self.notReset(sim):
            d = self.data.popleft()
            if d is NOP:
                self.doWrite(sim, None)
                self.doWriteVld(sim.write, 0)
            else:
                self.doWrite(sim, d)
                self.doWriteVld(sim.write, 1)
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, wrote, %d: %r\n" % (
                        self.intf._getFullName(),
                        sim.now, self.actualData))

        else:
            self.doWrite(sim, None)
            self.doWriteVld(sim.write, 0)
