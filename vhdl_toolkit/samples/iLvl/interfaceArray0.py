from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.interfaces.std import Ap_vld
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt
from vhdl_toolkit.intfLvl import connect


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

