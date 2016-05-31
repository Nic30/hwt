from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.interfaces.std import s
from hdl_toolkit.interfaces.utils import log2ceil


class FrameLink(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(32)
        
    def _declr(self):
        self.data = s(dtype=vecT(self.DATA_WIDTH))
        self.rem = s(dtype=vecT(log2ceil(self.DATA_WIDTH // 8)))
        self.src_rdy_n = s()
        self.dst_rdy_n = s(masterDir=DIRECTION.IN)
        self.sof_n = s()
        self.eof_n = s()
        self.eop_n = s()
        self.sop_n = s()
