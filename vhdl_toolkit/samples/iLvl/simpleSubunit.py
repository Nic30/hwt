from vhdl_toolkit.samples.iLvl.simple import SimpleUnit
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.interfaceLevel.interfaceUtils import connect

class SimpleSubunit(Unit):
    def _declr(self):
        self.subunit0 = SimpleUnit() 
        self.a = Ap_none(isExtern=True)
        self.b = Ap_none(isExtern=True)
        
    def _impl(self):
        u = self.subunit0
        connect(self.a, u.a)
        connect(u.b, self.b)
        

if __name__ == "__main__":
    print(synthetizeCls(SimpleSubunit))
