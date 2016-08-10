from hdl_toolkit.synthesizer.interfaceLevel.interface import Interface
from hdl_toolkit.synthesizer.param import Param
from hdl_toolkit.interfaces.amba import AxiStream
from hdl_toolkit.hdlObjects.specialValues import DIRECTION


class FullDuplexAxiStream(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        with self._paramsShared():
            self.tx = AxiStream()
            self.rx = AxiStream(masterDir=DIRECTION.IN)
