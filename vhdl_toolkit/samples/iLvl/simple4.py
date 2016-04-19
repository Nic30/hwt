from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT, hInt
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.interfaceLevel.interfaceUtils import connect



class SimpleUnit4(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(16)
        
    def _declr(self):
        dtype = vecT(self.DATA_WIDTH.opDiv(hInt(8)))
        self.a = Ap_none(dtype=dtype, isExtern=True)
        self.b = Ap_none(dtype=dtype, isExtern=True)
        
    def _impl(self):
        connect(self.a, self.b)


if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit4))
