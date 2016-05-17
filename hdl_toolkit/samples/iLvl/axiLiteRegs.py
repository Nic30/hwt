from hdl_toolkit.intfLvl import Unit
from hdl_toolkit.interfaces.amba import AxiLite, RESP_OKAY
from hdl_toolkit.interfaces.std import Ap_clk, Ap_none, Ap_rst_n, Ap_vld
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.synthetisator.rtlLevel.signalUtils import connectSig, And
from hdl_toolkit.hdlObjects.typeDefs import Enum, BIT
from hdl_toolkit.synthetisator.shortcuts import toRtl
from hdl_toolkit.hdlObjects.typeShortcuts import vec, vecT
from hdl_toolkit.synthetisator.param import Param, evalParam


class AxiLiteRegs(Unit):
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(32)
        self.IN_SUFFIX = "_in"
        self.OUT_SUFFIX = "_out"
        
        self.ADRESS_MAP = [
                           (0x0, "data"),
                           (0x4, "data2"),
                           (0x8, "data3"),
                           (0x12, "data4"),
                           ]
    
    def _declr(self):
        assert(len(self.ADRESS_MAP) > 0)
        self.clk = Ap_clk(isExtern=True)
        self.rst_n = Ap_rst_n(isExtern=True)
        
        self.axi = AxiLite(isExtern=True)
        
        for _, name in self.ADRESS_MAP:
            out = Ap_vld(isExtern=True)
            setattr(self, name + self.OUT_SUFFIX, out)
            
            _in = Ap_none(dtype=vecT(self.DATA_WIDTH), isExtern=True)
            setattr(self, name + self.IN_SUFFIX, _in)

        self._shareAllParams()
    
    
    
    def readPart(self):
        c = connectSig
        sig = self._sig
        reg = self._reg
        
        addrWidth = evalParam(self.ADDR_WIDTH).val
        dataWidth = evalParam(self.DATA_WIDTH).val
        
        rSt_t = Enum('rSt_t', ['rdIdle', 'rdData'])
        
        ar = self.axi.ar
        r = self.axi.r

        ar_hs = sig('ar_hs')
        arAddr = reg('arAddr', ar.addr._dtype) 
        rSt = reg('rSt', rSt_t, rSt_t.rdIdle)
        arRd = sig('arRd')
        rVld = sig('rVld')
        
        c(rSt.opEq(rSt_t.rdIdle), arRd)
        c(arRd, ar.ready)
        c(And(ar.valid, arRd), ar_hs)
        
        c(rSt.opEq(rSt_t.rdData), rVld)
        c(rVld, r.valid)
        c(vec(RESP_OKAY, 2), r.resp)
        
        # save ar addr
        If(And(arRd.opIsOn(), ar.valid._sig.opIsOn()),
            c(ar.addr, arAddr)
            ,
            c(arAddr, arAddr)
        )
        
        
        
        # ar fsm next
        If(arRd.opIsOn(),
           # rdIdle
            If(ar.valid._sig.opIsOn(),
               c(rSt_t.rdData, rSt) 
               ,
               c(rSt_t.rdIdle, rSt)
            )
            ,
            # rdData
            If(And(r.ready, rVld),
               c(rSt_t.rdIdle, rSt)
               ,
               c(rSt_t.rdData, rSt) 
            )
        )
        
        # build read data output mux
        rAssigTop = None
        for addr, name in self.ADRESS_MAP:
            _in = getattr(self, name + self.IN_SUFFIX)
            if rAssigTop is None:
                # data response
                rAssigTop = If(ar.addr._sig.opEq(vec(addr, addrWidth)),
                               c(_in, r.data)
                               ,
                               c(vec(0, dataWidth), r.data)
                            )
            else:
                rAssigTop = If(ar.addr._sig.opEq(vec(addr, addrWidth)),
                               c(_in, r.data)
                               ,
                               rAssigTop
                            )
                
        If(ar_hs.opIsOn(),
           rAssigTop
        )

    
    def writePart(self):
        c = connectSig
        sig = self._sig
        reg = self._reg
        addrWidth = evalParam(self.ADDR_WIDTH).val
        
        wSt_t = Enum('wSt_t', ['wrIdle', 'wrData', 'wrResp'])
        aw = self.axi.aw
        w = self.axi.w
        b = self.axi.b
        
        wSt = reg('wSt', wSt_t, wSt_t.wrIdle)
        awRd = sig('awRd')
        aw_hs = sig('aw_hs')
        awAddr = reg('awAddr', aw.addr._dtype) 
        wRd = sig('wRd')
        w_hs = sig('w_hs')
        c(wSt.opEq(wSt_t.wrResp), b.valid)
  
        c(wSt.opEq(wSt_t.wrIdle), awRd)
        c(awRd, aw.ready)
        c(wSt.opEq(wSt_t.wrData), wRd)
        c(wRd, w.ready)
        
        c(vec(RESP_OKAY, 2), self.axi.b.resp)
        c(wSt.opEq(wSt_t.wrResp))
        c(And(aw.valid, awRd), aw_hs) 
        c(And(w.valid, wRd), w_hs)
        
        # save aw addr
        If(And(awRd.opIsOn(), aw.valid._sig.opIsOn()),
            c(aw.addr, awAddr)
            ,
            c(awAddr, awAddr)
        )
        
        # write fsm
        If(wSt.opEq(wSt_t.wrIdle),  # wrIdle
            If(aw.valid._sig.opIsOn(),
                c(wSt_t.wrData, wSt)
                ,
                c(wSt, wSt)
            )
            ,
            If(wSt.opEq(wSt_t.wrData),  # wrData
                If(w.valid._sig.opIsOn(),
                    c(wSt_t.wrResp, wSt)
                    ,
                    c(wSt, wSt)
                )
                ,  # wrResp
                If(self.axi.b.ready._sig.opIsOn(),
                    c(wSt_t.wrIdle, wSt)
                    ,
                    c(wSt, wSt)
                )
            )
        )
        
        for addr, name in self.ADRESS_MAP:
            out = getattr(self, name + self.OUT_SUFFIX)
            c(w.data, out.data)
            c(And(w_hs, awAddr.opEq(vec(addr, addrWidth))), out.vld)
    
    def _impl(self):
        self.readPart()
        self.writePart()
        
        

if __name__ == "__main__":
    print(toRtl(AxiLiteRegs))
    
