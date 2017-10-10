from collections import deque

from hwt.hdl.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase


class RdSyncedAgent(SyncAgentBase):
    """
    Simulation/verification agent for RdSynced interface
    """
    def __init__(self, intf, allowNoReset=True):
        super().__init__(intf, allowNoReset=allowNoReset)
        self.actualData = NOP
        self.data = deque()
        self._rd = self.getRd(intf)

    def getRd(self, intf):
        return intf.rd

    def isRd(self, readFn):
        return readFn(self._rd)

    def wrRd(self, writeFn, val):
        writeFn(val, self._rd)

    def setEnable_asMonitor(self, en, sim):
        super(RdSyncedAgent, self).setEnable_asMonitor(en, sim)
        if not en:
            self.wrRd(sim.write, 0)

    def monitor(self, sim):
        """Collect data from interface"""
        if self.notReset(sim) and self._enabled:
            self.wrRd(sim.write, 1)

            yield sim.waitOnCombUpdate()

            d = self.doRead(sim)
            self.data.append(d)
        else:
            self.wrRd(sim.write, 0)

    def doRead(self, sim):
        """extract data from interface"""
        return sim.read(self.intf.data)

    def doWrite(self, sim, data):
        """write data to interface"""
        sim.write(data, self.intf.data)

    def driver(self, sim):
        """Push data to interface"""
        r = sim.read
        if self.actualData is NOP and self.data:
            self.actualData = self.data.popleft()

        do = self.actualData is not NOP

        if do:
            self.doWrite(sim, self.actualData)
        else:
            self.doWrite(sim, None)

        en = self.notReset(sim) and self._enabled
        if not (en and do):
            return

        yield sim.waitOnCombUpdate()

        rd = self.isRd(r)
        if en:
            assert rd.vldMask, (("%r: ready signal for interface %r is in invalid state,"
                                 " this would cause desynchronization") %
                                 (sim.now, self.intf))
        if rd.val:
            if self._debugOutput is not None:
                self._debugOutput.write("%s, wrote, %d: %r\n" % (
                                           self.intf._getFullName(),
                                           sim.now, self.actualData))
            if self.data:
                self.actualData = self.data.popleft()
            else:
                self.actualData = NOP
