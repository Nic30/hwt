from collections import deque

from hwt.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase
from hwtSimApi.hdlSimulator import HdlSimulator
from hwtSimApi.triggers import WaitCombRead, WaitWriteOnly, WaitCombStable
from pyMathBitPrecise.bit_utils import ValidityError


class HwIODataVldAgent(SyncAgentBase):

    def __init__(self, sim: HdlSimulator, hwIO: "HwIODataVld", allowNoReset=False):
        super(HwIODataVldAgent, self).__init__(
            sim,
            hwIO,
            allowNoReset=allowNoReset)
        self.data = deque()
        self._vld = self.get_valid_signal(hwIO)

    def get_data(self):
        return self.hwIO.data.read()

    def set_data(self, data):
        self.hwIO.data.write(data)

    @classmethod
    def get_valid_signal(cls, hwIO):
        return hwIO.vld

    def get_valid(self):
        return self._vld.read()

    def set_valid(self, val):
        self._lastVld = val
        return self._vld.write(val)

    def setEnable_asDriver(self, en):
        super(HwIODataVldAgent, self).setEnable_asDriver(en)
        if not en:
            self.set_valid(0)

    def monitor(self):
        yield WaitCombStable()
        if self.notReset():
            hwIO = self.hwIO
            vld = self.get_valid()
            try:
                vld = int(vld)
            except ValidityError:
                raise ValidityError(self.sim.now, hwIO._getFullName(),
                                    "vld signal in invalid state (would cause desynchronisation)")
            if vld:
                d = self.get_data()
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, read, %d: %r\n" % (
                        hwIO._getFullName(),
                        self.sim.now, d))
                self.data.append(d)

    def driver(self):
        yield WaitCombRead()
        if self.data and self.notReset():
            d = self.data.popleft()
        else:
            d = NOP

        yield WaitWriteOnly()
        if d is NOP:
            self.set_data(None)
            self.set_valid(0)
        else:
            self.set_data(d)
            self.set_valid(1)
            if self._debugOutput is not None:
                self._debugOutput.write("%s, wrote, %d: %r\n" % (
                    self.hwIO._getFullName(),
                    self.sim.now, self.actualData))
