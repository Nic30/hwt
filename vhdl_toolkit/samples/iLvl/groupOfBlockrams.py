from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.param import Param, shareAllParams
from vhdl_toolkit.samples.iLvl.bram import Bram
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls

@shareAllParams
class GroupOfBlockrams(Unit):
    ADDR_WIDTH = Param(32)
    DATA_WIDTH = Param(64)
    bramR = Bram()
    bramW = Bram()
    
    ap_clk = Ap_none(bramR.a.clk, bramR.b.clk, \
                     bramW.a.clk, bramW.b.clk, \
                     isExtern=True)
    we = Ap_none(bramR.a.we, bramR.b.we, \
                 bramW.a.we, bramW.b.we, \
                 isExtern=True)
    addr = Ap_none(bramR.a.addr, bramR.b.addr, \
                   bramW.a.addr, bramW.b.addr, \
                   dtype=vecT(ADDR_WIDTH), isExtern=True)
    
    in_w_a = Ap_none(bramW.a.din, dtype=vecT(DATA_WIDTH), isExtern=True)
    in_w_b = Ap_none(bramW.b.din, dtype=vecT(DATA_WIDTH), isExtern=True)
    in_r_a = Ap_none(bramR.a.din, dtype=vecT(DATA_WIDTH), isExtern=True)
    in_r_b = Ap_none(bramR.b.din, dtype=vecT(DATA_WIDTH), isExtern=True)
    
    out_w_a = Ap_none(src=bramW.a.dout, dtype=vecT(DATA_WIDTH), isExtern=True)
    out_w_b = Ap_none(src=bramW.b.dout, dtype=vecT(DATA_WIDTH), isExtern=True)
    out_r_a = Ap_none(src=bramR.a.dout, dtype=vecT(DATA_WIDTH), isExtern=True)
    out_r_b = Ap_none(src=bramR.b.dout, dtype=vecT(DATA_WIDTH), isExtern=True)

if __name__ == "__main__":
    print(synthetizeCls(GroupOfBlockrams))
