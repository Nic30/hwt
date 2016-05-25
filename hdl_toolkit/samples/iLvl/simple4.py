from hdl_toolkit.intfLvl import connect, Param, Unit
from hdl_toolkit.interfaces.std import Ap_none
from hdl_toolkit.hdlObjects.typeShortcuts import vecT, hInt



class SimpleUnit4(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(16)
        
    def _declr(self):
        dtype = vecT(self.DATA_WIDTH // hInt(8))
        self.a = Ap_none(dtype=dtype, isExtern=True)
        self.b = Ap_none(dtype=dtype, isExtern=True)
        
    def _impl(self):
        connect(self.a, self.b)


if __name__ == "__main__":
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    print(toRtl(SimpleUnit4))
