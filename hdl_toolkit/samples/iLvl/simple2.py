from hdl_toolkit.intfLvl import connect, Param, Unit
from hdl_toolkit.interfaces.amba import AxiStream
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls


class SimpleUnit2(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)

    def _declr(self):
        self.a = AxiStream(isExtern=True)
        self.b = AxiStream(isExtern=True)
        self._shareAllParams()
        
    def _impl(self):
        connect(self.a, self.b)

if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit2))