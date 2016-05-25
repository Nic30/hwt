from hdl_toolkit.intfLvl import connect, Unit
from hdl_toolkit.hdlObjects.typeDefs import BIT
from hdl_toolkit.interfaces.std import Ap_rst, Ap_none, Ap_clk

c = connect

class ClkSynchronizer(Unit):
    """
    Signal synchronization between two clock domains
    http://www.sunburst-design.com/papers/CummingsSNUG2008Boston_CDC.pdf
    """
    
    def _config(self):
        self.DATA_TYP = BIT
        
    def _declr(self):
        self.rst = Ap_rst()
        
        self.inData = Ap_none(dtype=self.DATA_TYP)
        self.inClk = Ap_clk()
        
        self.outData = Ap_none(dtype=self.DATA_TYP)
        self.outClk = Ap_clk()
        
        self._mkIntfExtern()
        
    def _impl(self):
        def reg(name, clk):
            return self._cntx.sig(name, self.DATA_TYP, clk=clk, syncRst=self.rst, defVal=0)
        inReg =   reg("inReg",   self.inClk )
        outReg0 = reg("outReg0", self.outClk)
        outReg1 = reg("outReg1", self.outClk)
        
        
        c(self.inData, inReg)
        
        c(inReg, outReg0)
        c(outReg0, outReg1)
        
        c(outReg1, self.outData)
        
if __name__ == "__main__":
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    print(toRtl(ClkSynchronizer))