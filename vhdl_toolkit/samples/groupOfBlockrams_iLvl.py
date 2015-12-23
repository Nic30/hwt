from vhdl_toolkit.synthetisator.interfaceLevel.synthetizator import Unit
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import Ap_none

class Bram(Unit):
    _origin = "dualportRAM.vhd"

class GroupOfBlockrams(Unit):
    bramR = Bram()
    bramW = Bram()
    ap_clk = Ap_none(bramR.a.clk, bramR.b.clk,\
                     bramW.a.clk, bramW.b.clk,\
                     isExtern=True)
    we = Ap_none(bramR.a.we, bramR.b.we,\
                 bramW.a.we, bramW.b.we,\
                 isExtern=True)
    r_a_addr = Ap_none(bramR.a.addr, isExtern=True)
    r_b_addr = Ap_none(bramR.b.addr, isExtern=True)
    w_a_addr = Ap_none(bramW.a.addr, isExtern=True)
    w_b_addr = Ap_none(bramW.b.addr, isExtern=True)
    out_w_a = Ap_none(src=bramW.a.dout, isExtern=True)
    out_w_b = Ap_none(src=bramW.b.dout, isExtern=True)
    out_r_a = Ap_none(src=bramR.a.dout, isExtern=True)
    out_r_b = Ap_none(src=bramR.b.dout, isExtern=True)

if __name__ == "__main__":
    u = GroupOfBlockrams()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise("GroupOfBlockrams")])
                     ))