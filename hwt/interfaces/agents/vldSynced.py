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

    def doRead(self):
        return self.intf.data.read()

    def doWrite(self, data):
        self.intf.data.write(data)

    def doReadVld(self):
        return self.intf.vld.read()

    def doWriteVld(self, val):
        self._lastVld = val
        return self.intf.vld.write(val)

    def setEnable_asDriver(self, en):
        super(VldSyncedAgent, self).setEnable_asDriver(en)
        if not en:
            self.wrVld(0)
        else:
            self.wrVld(self._lastVld)

    def monitor(self):
        yield WaitCombStable()
        if self.notReset():
            intf = self.intf
            vld = self.doReadVld()
            vld = int(vld)
            if vld:
                d = self.doRead()
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
            self.doWrite(None)
            self.doWriteVld(0)
        else:
            self.doWrite(d)
            self.doWriteVld(1)
            if self._debugOutput is not None:
                self._debugOutput.write("%s, wrote, %d: %r\n" % (
                    self.intf._getFullName(),
                    self.sim.now, self.actualData))
