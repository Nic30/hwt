from hwt.hwIOs.agents.signal import HwIOSignalAgent
from hwt.hwIOs.agents.vldSync import HwIODataVldAgent
from hwt.simulator.agentBase import SyncAgentBase
from hwtSimApi.agents.base import AgentBase


class HwIORegCntrlAgent(SyncAgentBase):
    """
    Simulation/verification agent for RegCntrl interface
    """

    def __init__(self, sim, hwIO: "HwIORegCntrl"):
        super().__init__(sim, hwIO)

        self._din = HwIOSignalAgent(sim, hwIO.din)
        self._dout = HwIODataVldAgent(sim, hwIO.dout, allowNoReset=True)

    def setEnable_asDriver(self, en: bool):
        AgentBase.setEnable(self, en)
        self._din.setEnable(en)
        self._dout.setEnable(en)

    def setEnable_asMonitor(self, en: bool):
        AgentBase.setEnable(self, en)
        self._din.setEnable(en)
        self._dout.setEnable(en)

    def din_getter(self):
        return self._din.data

    def din_setter(self, newVal):
        self._din.data = newVal

    din = property(din_getter, din_setter)

    def dout_getter(self):
        return self._dout.data

    def dout_setter(self, newVal):
        self._dout.data = newVal

    dout = property(dout_getter, dout_setter)

    def getDrivers(self):
        yield from self._din.getMonitors()
        yield from self._dout.getDrivers()

    def getMonitors(self):
        yield from self._din.getDrivers()
        yield from self._dout.getMonitors()
