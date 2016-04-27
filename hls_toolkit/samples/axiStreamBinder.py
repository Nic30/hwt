from hdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from hdl_toolkit.interfaces.amba import AxiStream
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls
from hdl_toolkit.interfaces.std import Ap_rst_n, Ap_clk
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.hdlObjects.typeShortcuts import hBit
from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.synthetisator.param import Param


def connectSig(a, b):
    if isinstance(a, Interface):
        a = a._sig
    b._src = a
    return b._sig.assignFrom(a)

def connectAxiStremSig(a, b):
    c = connectSig
    return [
        c(a.data, b.data),
        c(a.strb, b.strb),
        c(a.last, b.last),
        c(a.valid, b.valid),
        c(b.ready, a.ready)
    ]

def axiStreamDec(sel, in0, in1, out):
    If(sel.opEq(hBit(1)),
       connectAxiStremSig(in0, out) + [connectSig(hBit(0), in1.ready)],
       connectAxiStremSig(in1, out) + [connectSig(hBit(0), in0.ready)])


class AxiStreamBinder(Unit):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        self.clk = Ap_clk(isExtern=True)
        self.rst_n = Ap_rst_n(isExtern=True)
        
        self.dataIn0 = AxiStream(isExtern=True)
        self.dataIn1 = AxiStream(isExtern=True)
        self.dataOut = AxiStream(isExtern=True)
        self._shareAllParams()
        
    def _impl(self):
        ctx = self._cntx
        def syncBit(name): 
            return ctx.sig(name,
                           clk=self.clk._sig,
                           syncRst=self.rst_n._sig,
                           defVal=hBit(0))
        
        def cond2Log(cond, sig):
            return If(cond,
               [sig.assignFrom(hBit(1)) ],
               [sig.assignFrom(hBit(0)) ]
               )
        
        transInProgress = syncBit('transInProgress')
        prefer1 = syncBit('prefer1')
        
        outRd = self.dataOut.ready._sig
        in0vld = self.dataIn0.valid._sig
        in0last = self.dataIn0.last._sig
        
        in1vld = self.dataIn1.valid._sig
        in1last = self.dataIn1.last._sig
        
        axiStreamDec(prefer1, self.dataIn0, self.dataIn1, self.dataOut)
        
        If(transInProgress.opIsOn(),
            If(prefer1.opAnd(in1vld).opAnd(outRd).opAnd(in1last),
               [prefer1.assignFrom(hBit(0))],
               If(prefer1.opNot().opAnd(in0vld).opAnd(outRd).opAnd(in0last),
                  [prefer1.assignFrom(hBit(1))],
                  [prefer1.assignFrom(prefer1)]
                  )
               ),
           cond2Log(outRd.opAnd(in0vld.opOr(in1vld)), transInProgress)
        )
        
        
    
    
if __name__ == "__main__":
    print(synthetizeCls(AxiStreamBinder))
    
    
