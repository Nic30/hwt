from hwt.interfaces.std import HandshakeSync
from hwt.interfaces.structIntf import HdlType_to_Interface
from hwt.synthesizer.param import Param


class HsStructIntf(HandshakeSync):
    """
    A handshaked interface which has a data signal of type specified in configuration of this interface
    """

    def _config(self):
        self.T = Param(None)

    def _declr(self):
        assert self.T is not None
        self.data = HdlType_to_Interface().apply(self.T)
        HandshakeSync._declr(self)
