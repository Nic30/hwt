from vhdl_toolkit.synthetisator.interfaceLevel.synthetizator import Unit
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import Ap_none
from vhdl_toolkit.synthetisator.param import Param

class Bram(Unit):
    _origin = "dualportRAM.vhd"

class GroupOfBlockrams(Unit):
    ADDR_WIDTH = Param(32)
    DATA_WIDTH = Param(64)
    bramR = Bram()
    bramW = Bram()
    bramR.ADDR_WIDTH.inherieit(ADDR_WIDTH)
    bramR.DATA_WIDTH.inherieit(DATA_WIDTH)
    bramW.ADDR_WIDTH.inherieit(ADDR_WIDTH)
    bramW.DATA_WIDTH.inherieit(DATA_WIDTH)
    
    ap_clk = Ap_none(bramR.a.clk, bramR.b.clk, \
                     bramW.a.clk, bramW.b.clk, \
                     isExtern=True)
    we = Ap_none(bramR.a.we, bramR.b.we, \
                 bramW.a.we, bramW.b.we, \
                 isExtern=True)
    addr = Ap_none(bramR.a.addr, bramR.b.addr,\
                   bramW.a.addr, bramW.b.addr,\
                   width=ADDR_WIDTH, isExtern=True)
    in_w_a = Ap_none(bramW.a.din, width=DATA_WIDTH, isExtern=True)
    in_w_b = Ap_none(bramW.b.din, width=DATA_WIDTH, isExtern=True)
    in_r_a = Ap_none(bramR.a.din, width=DATA_WIDTH, isExtern=True)
    in_r_b = Ap_none(bramR.b.din, width=DATA_WIDTH, isExtern=True)
    
    out_w_a = Ap_none(src=bramW.a.dout, width=DATA_WIDTH, isExtern=True)
    out_w_b = Ap_none(src=bramW.b.dout, width=DATA_WIDTH, isExtern=True)
    out_r_a = Ap_none(src=bramR.a.dout, width=DATA_WIDTH, isExtern=True)
    out_r_b = Ap_none(src=bramR.b.dout, width=DATA_WIDTH, isExtern=True)

if __name__ == "__main__":
    u = GroupOfBlockrams()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise("GroupOfBlockrams")])
                     ))
