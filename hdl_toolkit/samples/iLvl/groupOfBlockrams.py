from hdl_toolkit.intfLvl import connect, Param, Unit
from hdl_toolkit.interfaces.std import Ap_none
from hdl_toolkit.samples.iLvl.bram import Bram
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls
from hdl_toolkit.hdlObjects.typeShortcuts import vecT

class GroupOfBlockrams(Unit):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        extData = lambda : Ap_none(dtype=vecT(self.DATA_WIDTH), isExtern=True)
        self.bramR = Bram()
        self.bramW = Bram()
        
        self.ap_clk = Ap_none(isExtern=True)
        self.we = Ap_none(isExtern=True)
        self.addr = Ap_none(dtype=vecT(self.ADDR_WIDTH), isExtern=True)
        self.in_w_a = extData()
        self.in_w_b = extData()
        self.in_r_a = extData()
        self.in_r_b = extData()
        
        self.out_w_a =extData()
        self.out_w_b =extData()
        self.out_r_a =extData()
        self.out_r_b =extData()
        self._shareAllParams()
    
    def _impl(self):
        s = self
        bramR = s.bramR
        bramW = s.bramW
        c = connect
        
        c(s.ap_clk,
            bramR.a.clk, bramR.b.clk,
            bramW.a.clk, bramW.b.clk)
        c(s.we,
            bramR.a.we, bramR.b.we,
            bramW.a.we, bramW.b.we)
        c(self.addr,
            bramR.a.addr, bramR.b.addr,
            bramW.a.addr, bramW.b.addr)
        
        c(s.in_w_a, bramW.a.din)
        c(s.in_w_b, bramW.b.din)
        c(s.in_r_a, bramR.a.din)
        c(s.in_r_b, bramR.b.din)
        c(bramW.a.dout, s.out_w_a)
        c(bramW.b.dout, s.out_w_b)
        c(bramR.a.dout, s.out_r_a)
        c(bramR.b.dout, s.out_r_b)
        

if __name__ == "__main__":
    print(synthetizeCls(GroupOfBlockrams))
