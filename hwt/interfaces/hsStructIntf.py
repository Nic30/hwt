from hwt.hdl.types.hdlType import HdlType
from hwt.interfaces.std import HandshakeSync
from hwt.interfaces.structIntf import HdlType_to_Interface
from hwt.synthesizer.param import Param
from hwt.interfaces.agents.handshaked import HandshakedAgent
from hwtSimApi.hdlSimulator import HdlSimulator


class HsStructIntf(HandshakeSync):
    """
    A handshaked interface which has a data signal of type specified in configuration of this interface
    """

    def _config(self):
        self.T: HdlType = Param(None)

    def _declr(self):
        assert isinstance(self.T, HdlType), self.T
        self.data = HdlType_to_Interface().apply(self.T)
        HandshakeSync._declr(self)

    def _initSimAgent(self, sim:HdlSimulator):
        self._ag = HsStructIntfAgent(sim, self)


class HsStructIntfAgent(HandshakedAgent):

    def __init__(self, sim:HdlSimulator, intf:"Handshaked", allowNoReset=False):
        HandshakedAgent.__init__(self, sim, intf, allowNoReset=allowNoReset)
        intf.data._initSimAgent(sim)
        self._data_ag = intf.data._ag

    def set_data(self, data):
        return self._data_ag.set_data(data)

    def get_data(self):
        return self._data_ag.get_data()
