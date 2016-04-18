from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.interfaceLevel.interface import connect

class SimpleWithNonDirectIntConncetion(Unit):
    def _declr(self):
        self.a = Ap_none(isExtern=True)
        self.b = Ap_none()
        self.c = Ap_none(isExtern=True)
        
    def _impl(self):
        connect(self.a, self.b)
        connect(self.b, self.c)

if __name__ == "__main__":
    print(synthetizeCls(SimpleWithNonDirectIntConncetion))
