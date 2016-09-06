from hdl_toolkit.simulator.agents.vldSynced import VldSyncedAgent
from hdl_toolkit.simulator.agents.signal import SignalAgent
from hdl_toolkit.simulator.agents.agentBase import SyncAgentBase


class RegCntrlAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        self.intf = intf
        if clk is None:
            clk = self._getClk()
        
        self._rx = SignalAgent(intf.din, clk=clk, rstn=None)
        self._tx = VldSyncedAgent(intf.dout, clk=clk, rstn=rstn, allowNoReset=True)

    def getDrivers(self):
        return self._rx.getMonitors() + self._tx.getDrivers()
    
    def getMonitors(self):
        return self._rx.getDrivers() + self._tx.getMonitors()