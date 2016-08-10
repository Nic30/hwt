from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.interfaces.std import s
from hdl_toolkit.synthesizer.interfaceLevel.interface import Interface
from hdl_toolkit.synthesizer.param import Param


class Mi32(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(32)
        self.ADDR_WIDTH = Param(32)
        
    def _declr(self):
        self.dwr = s(dtype=vecT(self.DATA_WIDTH))
        self.addr = s(dtype=vecT(self.ADDR_WIDTH))
        self.be = s(dtype=vecT(self.DATA_WIDTH // 8))
        self.rd = s()
        self.wr = s()
        self.ardy = s(masterDir=DIRECTION.IN)
        self.drd = s(dtype=vecT(self.DATA_WIDTH), masterDir=DIRECTION.IN)
        self.drdy = s(masterDir=DIRECTION.IN)
