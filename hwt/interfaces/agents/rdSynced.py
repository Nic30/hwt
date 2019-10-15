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

    def isRd(self):
        return self._rd.read()

    def wrRd(self, val):
        self._rd.write(val)

    def setEnable_asMonitor(self, en, sim):
        super(RdSyncedAgent, self).setEnable_asMonitor(en, sim)
        if not en:
            self.wrRd(0)

    def monitor(self, sim):
        """Collect data from interface"""
        yield WaitCombRead()
        if self.notReset() and self._enabled:
            yield WaitWriteOnly()
            self.wrRd(1)

            yield WaitCombRead()
            d = self.doRead()
            self.data.append(d)
        else:
            yield WaitWriteOnly()
            self.wrRd(0)

    def doRead(self, sim):
        """extract data from interface"""
        return self.intf.data.read()

    def doWrite(self, sim, data):
        """write data to interface"""
        self.intf.data.write(data)

    def driver(self, sim):
        """Push data to interface"""
        yield WaitWriteOnly()
        if self.actualData is NOP and self.data:
            self.actualData = self.data.popleft()

        do = self.actualData is not NOP

        if do:
            self.doWrite(sim, self.actualData)
        else:
            self.doWrite(sim, None)

        yield WaitCombRead()
        en = self.notReset() and self._enabled
        if not (en and do):
            return

        if en:
            rd = self.isRd()
            try:
                rd = int(rd)
            except ValueError:
                raise AssertionError(
                    ("%r: ready signal for interface %r is in invalid state,"
                     " this would cause desynchronization") %
                    (sim.now, self.intf))
            if rd:
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, wrote, %d: %r\n" % (
                                               self.intf._getFullName(),
                                               sim.now, self.actualData))
                if self.data:
                    self.actualData = self.data.popleft()
                else:
                    self.actualData = NOP
