from vhdl_toolkit.synthetisator.interfaceLevel.interface import  Interface, IfConfMap, IfConfig
from vhdl_toolkit.types import DIRECTION

D = DIRECTION

c = IfConfMap

class Ap_clk(Interface):
        CLK = c("ap_clk", masterDir=D.OUT, width=1)

class BramPort(Interface):
    ADDR_WIDTH = 32
    DATA_WIDTH = 64 
    clk = c("_clk", masterDir=D.OUT, width=1)
    addr = c("_addr", masterDir=D.OUT, width=ADDR_WIDTH)
    din = c("_din", masterDir=D.OUT, width=DATA_WIDTH)
    dout = c("_dout", masterDir=D.IN, width=DATA_WIDTH)
    # en = c("_en", masterDir=D.OUT, width=1)
    we = c("_we", masterDir=D.OUT, width=1)   
    
    
allInterfaces = [Ap_clk, BramPort]
