from hdl_toolkit.interfaces.agents.signal import SignalAgent
from hdl_toolkit.interfaces.agents.vldSynced import VldSyncedAgent
from hdl_toolkit.simulator.agentBase import SyncAgentBase


class RegCntrlAgent(SyncAgentBase):
    def __init__(self, intf, clk=None, rstn=None):
        self.intf = intf
        if clk is None:
            clk = self._getClk()
        
        self._din = SignalAgent(intf.din, clk=clk, rstn=None)
        self._dout = VldSyncedAgent(intf.dout, clk=clk, rstn=rstn, allowNoReset=True)

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