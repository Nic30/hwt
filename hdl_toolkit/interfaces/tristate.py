from hdl_toolkit.synthesizer.interfaceLevel.interface import Interface
from hdl_toolkit.synthesizer.param import Param
from hdl_toolkit.interfaces.std import Signal
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.specialValues import DIRECTION

class TristateSig(Interface):
    """
    Tristate interface
    """
    def _config(self):
        self.DATA_WIDTH = Param(1)
        self.forceVector = False
        
    def _declr(self):
        t = Bits((self.DATA_WIDTH-1)._downto(0), self.forceVector)
        
        self.t = Signal(dtype=t) # connect
        self.i = Signal(dtype=t, masterDir=DIRECTION.IN) # input
        self.o = Signal(dtype=t) # output

class TristateClk(TristateSig):
    pass