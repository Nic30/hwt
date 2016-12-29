from hwt.synthesizer.interfaceLevel.interface import Interface
from hwt.synthesizer.param import Param
from hwt.interfaces.std import Signal
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.constants import DIRECTION

class TristateSig(Interface):
    """
    Tristate interface
    in order to make this a vector[0] instead of single bit use forceVector=True
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