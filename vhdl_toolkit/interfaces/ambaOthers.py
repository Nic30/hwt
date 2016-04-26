from vhdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION, INTF_DIRECTION


class FullDuplexAxiStream(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        self.tx = AxiStream()
        self.rx = AxiStream(masterDir=DIRECTION.IN)
