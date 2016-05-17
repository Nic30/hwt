from hdl_toolkit.interfaces.std import Ap_vld
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls
from hdl_toolkit.hdlObjects.typeShortcuts import hInt
from hdl_toolkit.intfLvl import connect, Unit, Param

class SimpleSubunit(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        
    def _declr(self):
        self.c = Ap_vld(isExtern=True)
        self.d = Ap_vld(isExtern=True)
        self._shareAllParams()
        
    def _impl(self):
        connect(self.c, self.d)

class InterfaceArraySample(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        
    def _declr(self):
        LEN = hInt(2)
        self.a = Ap_vld(multipliedBy=LEN, isExtern=True)
        self.b = Ap_vld(multipliedBy=LEN, isExtern=True)
    
        self.u0 = SimpleSubunit() 
        self.u1 = SimpleSubunit()
        # self.u2 = SimpleSubunit()
        self._shareAllParams()
        
    def _impl(self):
        
        connect(self.a[0], self.u0.c)
        connect(self.a[1], self.u1.c)
        # u2in = connect(a[2], u2.c)
    
        connect(self.u0.d, self.b[0])
        connect(self.u1.d, self.b[1])
        # u2out = connect(u2.d, b[2])

if __name__ == "__main__":
    print(
    synthetizeCls(InterfaceArraySample)
    )
