from hdl_toolkit.intfLvl import Param, connect, Unit
from hdl_toolkit.interfaces.amba import AxiStream


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
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    print(toRtl(Simple2withNonDirectIntConnection))
