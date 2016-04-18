from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.interfaceLevel.interface import connect

class SimpleSubunit3(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(128)
        
    def _declr(self):
        self.subunit0 = SimpleUnit2() 
        self.a0 = AxiStream(isExtern=True)
        self.b0 = AxiStream(isExtern=True)
        self._shareAllParams()
        
    def _impl(self):
        u = self.subunit0
        connect(self.a0, u.a)
        connect(u.b, self.b0)

if __name__ == "__main__":
    print(synthetizeCls(SimpleSubunit3))
