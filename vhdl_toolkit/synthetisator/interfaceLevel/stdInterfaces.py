from vhdl_toolkit.synthetisator.interfaceLevel.interface import  Interface, IfConfMap, IfConfig


c = IfConfMap

class Ap_clk(Interface):
        CLK = c("ap_clk", masterDir=IfConfig.dir_out, width=1)

class BramPort(Interface):
    ADDR_WIDTH = 32
    DATA_WIDTH = 64 
    clk = c("_clk", masterDir=IfConfig.dir_out, width=1)
    addr = c("_addr", masterDir=IfConfig.dir_out, width=ADDR_WIDTH)
    din = c("_din", masterDir=IfConfig.dir_out, width=DATA_WIDTH)
    dout = c("_dout", masterDir=IfConfig.dir_in, width=DATA_WIDTH)
    #en = c("_en", masterDir=IfConfig.dir_out, width=1)
    we = c("_we", masterDir=IfConfig.dir_out, width=1)   
    
    
allInterfaces = [Ap_clk, BramPort]