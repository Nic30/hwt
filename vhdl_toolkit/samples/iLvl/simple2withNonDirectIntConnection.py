from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.interfaceLevel.interfaceUtils import connect


class Simple2withNonDirectIntConnection(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        
    def _declr(self):
        self.a = AxiStream(isExtern=True)
        self.c = AxiStream(isExtern=True)
        self.b = AxiStream()
        self._shareAllParams()
        
    def _impl(self):
        b = self.b
        connect(self.a, b)
        connect(b, self.c)
        
if __name__ == "__main__":
    print(synthetizeCls(Simple2withNonDirectIntConnection))
