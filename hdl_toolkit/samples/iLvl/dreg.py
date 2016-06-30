from hdl_toolkit.intfLvl import connect, Unit
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.interfaces.std import Ap_rst, Ap_none, Ap_clk

c = connect

class DReg(Unit):
    def _declr(self):
        
        self.clk = Ap_clk()
        self.rst = Ap_rst()

        self.din = Ap_none(dtype=BIT)
        self.dout = Ap_none(dtype=BIT)
        
        self._mkIntfExtern()
        
    def _impl(self):

        internReg = self._reg("internReg", BIT, defVal=False)        
        
        c(self.din, internReg)
        c(internReg, self.dout)
        
if __name__ == "__main__":
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    print(toRtl(DReg))
