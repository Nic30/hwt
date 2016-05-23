import math

from hdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from hdl_toolkit.synthetisator.param import Param, evalParam
from hdl_toolkit.synthetisator.rtlLevel.signalUtils import connectSig
from hdl_toolkit.interfaces.amba import AxiStream
from hdl_toolkit.hdlObjects.typeShortcuts import vec, hBit, vecT
from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If, Switch
from hdl_toolkit.interfaces.std import Ap_clk, Ap_rst_n
from hdl_toolkit.synthetisator.shortcuts import toRtl

c = connectSig

class AxiStreamStoredBurst(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
        self.DATA = [ ord(c) for c in "Hello world" ]
        
    def writeData(self, d, vldMask, last):
        return c(vec(d, self.DATA_WIDTH), self.dataOut.data) + \
               c(vec(vldMask, self.DATA_WIDTH // 8), self.dataOut.strb) + \
               c(hBit(last), self.dataOut.last) + \
               c(hBit(True), self.dataOut.valid)
    
    def writeStop(self):
        return c(vec(0, self.DATA_WIDTH), self.dataOut.data) + \
               c(vec(0, self.DATA_WIDTH // 8), self.dataOut.strb) + \
               c(hBit(False), self.dataOut.last) + \
               c(hBit(False), self.dataOut.valid)
    
    def dataRd(self):
        return self.dataOut.ready._sig.opIsOn()
    
    def _declr(self):
        self.clk = Ap_clk()
        self.rst_n = Ap_rst_n()
        self.dataOut = AxiStream()
        self._shareAllParams()
        self._mkIntfExtern()
    
    def _impl(self):
        self.DATA_WIDTH = evalParam(self.DATA_WIDTH).val
        vldAll = Bitmask.mask(self.DATA_WIDTH//8)
        
        DATA_LEN = len(self.DATA)
        
        wordIndex_w = int(math.log2(len(self.DATA)) + 1)
        wordIndex = self._reg("wordIndex", vecT(wordIndex_w), defVal=0)
  
        Switch(wordIndex,
               *[(vec(i, wordIndex_w), 
                  self.writeData(d, vldAll, i == DATA_LEN -1) +
                  If(self.dataRd(),
                      c(vec(i+1, wordIndex_w), wordIndex)
                      ,
                      c(wordIndex, wordIndex)
                  )
                 ) for i, d in enumerate(self.DATA)],
               (None, self.writeStop())
        )
            
        
        
if __name__ == "__main__":
    print(toRtl(AxiStreamStoredBurst))
