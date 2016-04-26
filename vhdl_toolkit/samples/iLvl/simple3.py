from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.intfLvl import connect, Param, Unit
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT



class SimpleUnit3(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        
    def _declr(self):
        dt = vecT(self.DATA_WIDTH)
        self.a = Ap_none(dtype=dt, isExtern=True)
        self.b = Ap_none(dtype=dt, isExtern=True)
        
    def _impl(self):
        connect(self.a, self.b)
        
        
if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit3))
