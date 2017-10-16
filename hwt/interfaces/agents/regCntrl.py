from hwt.interfaces.agents.signal import SignalAgent
from hwt.interfaces.agents.vldSynced import VldSyncedAgent
from hwt.simulator.agentBase import SyncAgentBase, AgentBase


class RegCntrlAgent(SyncAgentBase):
    """
    Simulation/verification agent for RegCntrl interface
    """

    def __init__(self, intf):
        AgentBase.__init__(self, intf)
        super().__init__(intf)

        self._din = SignalAgent(intf.din)
        self._dout = VldSyncedAgent(intf.dout, allowNoReset=True)

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
        return self._din.getMonitors() + self._dout.getDrivers()

    def getMonitors(self):
        return self._din.getDrivers() + self._dout.getMonitors()
