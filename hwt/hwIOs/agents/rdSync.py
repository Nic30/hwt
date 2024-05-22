from collections import deque

from hwt.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase
from hwtSimApi.hdlSimulator import HdlSimulator
from hwtSimApi.triggers import WaitCombRead, WaitWriteOnly


class HwIODataRdAgent(SyncAgentBase):
    """
    Simulation/verification agent for RdSynced interface
    """
    def __init__(self, sim: HdlSimulator, hwIO: "HwIODataRd", allowNoReset=True):
        super().__init__(sim, hwIO, allowNoReset=allowNoReset)
        self.actualData = NOP
        self.data = deque()
        self._rd = self.get_ready_signal(hwIO)

    @classmethod
    def get_ready_signal(cls, hwIO: "HwIODataRd"):
        return hwIO.rd

    def get_ready(self):
        return self._rd.read()

    def set_ready(self, val):
        self._rd.write(val)

    def setEnable_asMonitor(self, en: bool):
        super(HwIODataRdAgent, self).setEnable_asMonitor(en)
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
        return self.hwIO.data.read()

    def set_data(self, data):
        """write data to interface"""
        self.hwIO.data.write(data)

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
                    (self.sim.now, self.hwIO))
            if rd:
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, wrote, %d: %r\n" % (
                                               self.hwIO._getFullName(),
                                               self.sim.now, self.actualData))
                if self.data:
                    self.actualData = self.data.popleft()
                else:
                    self.actualData = NOP
