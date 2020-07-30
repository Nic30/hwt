from collections import deque

from hwt.hdl.constants import NOP
from hwt.simulator.agentBase import SyncAgentBase
from pycocotb.hdlSimulator import HdlSimulator
from pycocotb.triggers import WaitCombRead, WaitWriteOnly, WaitCombStable


class VldSyncedAgent(SyncAgentBase):

    def __init__(self, sim: HdlSimulator, intf, allowNoReset=False):
        super(VldSyncedAgent, self).__init__(
            sim,
            intf,
            allowNoReset=allowNoReset)
        self.data = deque()
        self._vld = self.get_valid_signal(intf)

    def get_data(self):
        return self.intf.data.read()

    def set_data(self, data):
        self.intf.data.write(data)

    @classmethod
    def get_valid_signal(cls, intf):
        return intf.vld

    def get_valid(self):
        return self._vld.read()

    def set_valid(self, val):
        self._lastVld = val
        return self._vld.write(val)

    def setEnable_asDriver(self, en):
        super(VldSyncedAgent, self).setEnable_asDriver(en)
        if not en:
            self.set_valid(0)

    def monitor(self):
        yield WaitCombStable()
        if self.notReset():
            intf = self.intf
            vld = self.get_valid()
            vld = int(vld)
            if vld:
                d = self.get_data()
                if self._debugOutput is not None:
                    self._debugOutput.write("%s, read, %d: %r\n" % (
                        intf._getFullName(),
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
                    self.intf._getFullName(),
                    self.sim.now, self.actualData))
