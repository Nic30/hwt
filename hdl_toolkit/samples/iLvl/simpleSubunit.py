from hdl_toolkit.intfLvl import connect, Unit
from hdl_toolkit.interfaces.std import Ap_none
from hdl_toolkit.samples.iLvl.simple import SimpleUnit

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
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    print(toRtl(SimpleSubunit))
