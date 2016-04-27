from hdl_toolkit.intfLvl import connect, Unit, Param
from hdl_toolkit.interfaces.std import Ap_vld
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls
from hdl_toolkit.hdlObjects.typeShortcuts import hInt


class InterfaceArraySample(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        self.LEN = hInt(3)
    
    def _declr(self):
        self.a = Ap_vld(multipliedBy=self.LEN, isExtern=True)
        self.b = Ap_vld(multipliedBy=self.LEN, isExtern=True)
        self._shareAllParams()
    
    def _impl(self):
        connect(self.a, self.b)


if __name__ == "__main__":
    print(synthetizeCls(InterfaceArraySample))

