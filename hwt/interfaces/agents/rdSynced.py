from collections import deque

from hwt.hdl.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.triggers import WaitCombRead, WaitWriteOnly


class RdSyncedAgent(SyncAgentBase):
    """
    Simulation/verification agent for RdSynced interface
    """
    def __init__(self, sim: HdlSimulator, intf, allowNoReset=True):
        super().__init__(sim, intf, allowNoReset=allowNoReset)
        self.actualData = NOP
        self.data = deque()
        self._rd = self.get_ready_signal(intf)

    @classmethod
    def get_ready_signal(cls, intf):
        return intf.rd

    def get_ready(self):
        return self._rd.read()

    def set_ready(self, val):
        self._rd.write(val)

    def setEnable_asMonitor(self, en):
        super(RdSyncedAgent, self).setEnable_asMonitor(en)
        if not en:
            self.set_ready(0)

    def monitor(self):
        """Collect data from interface"""
        yield WaitCombRead()
        if self.notReset() and self._enabled:
            yield WaitWriteOnly()
            self.set_ready(1)

            yield WaitCombRead()
            d = self.get_data()
            self.data.append(d)
        else:
            yield WaitWriteOnly()
            self.set_ready(0)

    def get_data(self):
        """extract data from interface"""
        return self.intf.data.read()

    def set_data(self, data):
        """write data to interface"""
        self.intf.data.write(data)

    def driver(self):
        """Push data to interface"""
        yield WaitWriteOnly()
        if self.actualData is NOP and self.data:
            self.actualData = self.data.popleft()

        do = self.actualData is not NOP

        if do:
            self.set_data(self.actualData)
        else:
            self.set_data(None)

        yield WaitCombRead()
        en = self.notReset() and self._enabled
        if not (en and do):
            return

        if en:
            rd = self.get_ready()
            try:
                rd = int(rd)
            except ValueError:
                raise AssertionError(
                    ("%r: ready signal for interface %r is in invalid state,"
                     " this would cause desynchronization") %
                    (self.sim.now, self.intf))
            if rd:
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, wrote, %d: %r\n" % (
                                               self.intf._getFullName(),
                                               self.sim.now, self.actualData))
                if self.data:
                    self.actualData = self.data.popleft()
                else:
                    self.actualData = NOP
