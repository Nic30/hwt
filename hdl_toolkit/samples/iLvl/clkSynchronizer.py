from hdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from hdl_toolkit.hdlObjects.typeDefs import BIT
from hdl_toolkit.synthetisator.rtlLevel.signalUtils import connectSig
from hdl_toolkit.interfaces.std import Ap_rst, Ap_none, Ap_clk
from hdl_toolkit.synthetisator.shortcuts import toRtl

c = connectSig

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
        inReg = self._cntx.sig("inReg", self.DATA_TYP, clk=self.inClk, syncRst=self.rst, defVal=0)
        outReg0 = self._cntx.sig("outReg0", self.DATA_TYP, clk=self.outClk, syncRst=self.rst, defVal=0)
        outReg1 = self._cntx.sig("outReg1", self.DATA_TYP, clk=self.outClk, syncRst=self.rst, defVal=0)
        
        
        c(self.inData, inReg)
        
        c(inReg, outReg0)
        c(outReg0, outReg1)
        
        c(outReg1, self.outData)
        
if __name__ == "__main__":
    print(toRtl(ClkSynchronizer))