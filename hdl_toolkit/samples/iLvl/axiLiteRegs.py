from hdl_toolkit.intfLvl import Unit, connect
from hdl_toolkit.interfaces.amba import AxiLite, RESP_OKAY
from hdl_toolkit.interfaces.std import Ap_clk, Ap_none, Ap_rst_n, Ap_vld
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If, Switch
from hdl_toolkit.hdlObjects.typeDefs import Enum
from hdl_toolkit.synthetisator.shortcuts import toRtl
from hdl_toolkit.hdlObjects.typeShortcuts import vec, vecT
from hdl_toolkit.synthetisator.param import Param, evalParam

c = connect
        
class AxiLiteRegs(Unit):
    """
    Axi lite register generator
    """
    def _config(self):
        self.ADDR_WIDTH = Param(8)
        self.DATA_WIDTH = Param(32)
        self.IN_SUFFIX = "_in"
        self.OUT_SUFFIX = "_out"
        
        self.ADRESS_MAP = [ 
                           *[(i * 4 , "data%d" % i) for i in range(4)]
                           
                           # (0x0, "data"),
                           # (0x4, "data2"),
                           # (0x8, "data3"),
                           # (0x12, "data4"),
                           ]
    
    def _declr(self):
        assert(len(self.ADRESS_MAP) > 0)
        
        self.clk = Ap_clk()
        self.rst_n = Ap_rst_n()
        
        self.axi = AxiLite()
        
        for _, name in self.ADRESS_MAP:
            out = Ap_vld()
            setattr(self, name + self.OUT_SUFFIX, out)
            
            _in = Ap_none(dtype=vecT(self.DATA_WIDTH))
            setattr(self, name + self.IN_SUFFIX, _in)

        self._mkIntfExtern()
        self._shareAllParams()
    
    def readPart(self):
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
        
        c(rSt._eq(rSt_t.rdIdle), arRd)
        c(arRd, ar.ready)
        c(ar.valid & arRd, ar_hs)
        
        c(rSt._eq(rSt_t.rdData), rVld)
        c(rVld, r.valid)
        c(vec(RESP_OKAY, 2), r.resp)
        
        # save ar addr
        If(arRd & ar.valid,
            c(ar.addr, arAddr)
            ,
            c(arAddr, arAddr)
        )
        
        
        
        # ar fsm next
        If(arRd,
           # rdIdle
            If(ar.valid,
               c(rSt_t.rdData, rSt) 
               ,
               c(rSt_t.rdIdle, rSt)
            )
            ,
            # rdData
            If(r.ready & rVld,
               c(rSt_t.rdIdle, rSt)
               ,
               c(rSt_t.rdData, rSt) 
            )
        )
        
        # build read data output mux
        def inputByName(name):
            return getattr(self, name + self.IN_SUFFIX)
            
        rAssigTop = Switch(ar.addr,
               *[(vec(addr, addrWidth), c(inputByName(name), r.data)) \
                      for addr, name in self.ADRESS_MAP],
               (None, c(vec(0, dataWidth), r.data)))
                
        If(ar_hs,
           rAssigTop
           ,
           c(vec(0, dataWidth), r.data)
        )

    
    def writePart(self):
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
        c(wSt._eq(wSt_t.wrResp), b.valid)
  
        c(wSt._eq(wSt_t.wrIdle), awRd)
        c(awRd, aw.ready)
        c(wSt._eq(wSt_t.wrData), wRd)
        c(wRd, w.ready)
        
        c(vec(RESP_OKAY, 2), self.axi.b.resp)
        c(aw.valid & awRd, aw_hs) 
        c(w.valid & wRd, w_hs)
        
        # save aw addr
        If(awRd & aw.valid,
            c(aw.addr, awAddr)
            ,
            c(awAddr, awAddr)
        )
        
        # write fsm
        Switch(wSt,
            (wSt_t.wrIdle,
                If(aw.valid,
                    c(wSt_t.wrData, wSt)
                    ,
                    c(wSt, wSt)
                )
            )
            ,
            (wSt_t.wrData,
                If(w.valid,
                    c(wSt_t.wrResp, wSt)
                    ,
                    c(wSt, wSt)
                )
            )
            ,
            (wSt_t.wrResp,
                If(self.axi.b.ready,
                    c(wSt_t.wrIdle, wSt)
                    ,
                    c(wSt, wSt)
                )
            )
        )
        
        # output vld
        for addr, name in self.ADRESS_MAP:
            out = getattr(self, name + self.OUT_SUFFIX)
            c(w.data, out.data)
            c(w_hs & (awAddr._eq(vec(addr, addrWidth))), out.vld)
    
    def _impl(self):
        self.readPart()
        self.writePart()
        
        

if __name__ == "__main__":
    print(toRtl(AxiLiteRegs))
    
