from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls, synthetizeAndSave
from vhdl_toolkit.intfLvl import connect, Unit


class SimpleUnit(Unit):
    def _declr(self):
        self.a = Ap_none(isExtern=True)
        self.b = Ap_none(isExtern=True)
    
    def _impl(self):
        connect(self.a, self.b)


if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit))
