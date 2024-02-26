from hwt.hdl.types.hdlType import HdlType
from hwt.interfaces.agents.rdSynced import RdSyncedAgent
from hwt.interfaces.std import RdSynced, Signal
from hwt.interfaces.structIntf import HdlType_to_Interface
from hwt.synthesizer.param import Param
from hwtSimApi.hdlSimulator import HdlSimulator
from ipCorePackager.constants import DIRECTION


class RdSyncedStructIntf(RdSynced):
    """
    A RdSynced interface which has a data signal of type specified in configuration of this interface
    """

    def _config(self):
        self.T: HdlType = Param(None)

    def _declr(self):
        assert isinstance(self.T, HdlType), (self.T, self._name)
        self._dtype = self.T
        self.data = HdlType_to_Interface().apply(self.T)
        self.rd = Signal(masterDir=DIRECTION.IN)

    def _initSimAgent(self, sim:HdlSimulator):
        self._ag = RdSyncedStructIntfAgent(sim, self)


class RdSyncedStructIntfAgent(RdSyncedAgent):

    def __init__(self, sim:HdlSimulator, intf:RdSyncedStructIntf, allowNoReset=False):
        RdSyncedAgent.__init__(self, sim, intf, allowNoReset=allowNoReset)
        intf.data._initSimAgent(sim)
        self._data_ag = intf.data._ag

    def set_data(self, data):
        return self._data_ag.set_data(data)

    def get_data(self):
        return self._data_ag.get_data()
