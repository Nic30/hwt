from vhdl_toolkit.synthetisator.interfaceLevel.synthetizator import Unit, Connection
from vhdl_toolkit.formater import formatVhdl


class Bram(Unit):
    _origin = "dualportRAM.vhd"

c = Connection


class SuperDMA(Unit):
    bramR = Bram()
    bramW = Bram()
    clk = c(bramR.a.clk, bramR.b.clk,\
            bramW.a.clk, bramW.b.clk,\
            hasExtern=True)
    we = c(bramR.a.we, bramR.b.we,\
           bramW.a.we, bramW.b.we,\
            hasExtern=True)
    r_a_addr = c(bramR.a.addr, hasExtern=True)
    r_b_addr = c(bramR.b.addr, hasExtern=True)
    w_a_addr = c(bramW.a.addr, hasExtern=True)
    w_b_addr = c(bramW.b.addr, hasExtern=True)


if __name__ == "__main__":
    dma = SuperDMA()
    print(formatVhdl(
                     "\n".join([ str(x) for x in dma._synthetize("superDma")])
                     ))