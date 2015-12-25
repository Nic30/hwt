from vhdl_toolkit.synthetisator.interfaceLevel.interface import  Interface
from vhdl_toolkit.types import DIRECTION
from vhdl_toolkit.synthetisator.param import Param

D = DIRECTION


class Ap_none(Interface):
    def __init__(self, *destinations, masterDir=D.OUT, width=1, src=None, isExtern=False):
        Interface.__init__(self, *destinations,masterDir=masterDir, src=src, isExtern=isExtern)
        self._width = width

        
s= Ap_none        

class Ap_clk(Interface):
    ap_clk = s(masterDir=D.OUT)
        
class Ap_hs(Interface):
    DATA_WIDTH = Param(64)
    data = s(masterDir=D.OUT, width=DATA_WIDTH)
    rd = s(masterDir=D.IN)
    vld = s(masterDir=D.OUT)

class BramPort(Interface):
    ADDR_WIDTH = Param(32)
    DATA_WIDTH = Param(64) 
    clk = s(masterDir=D.OUT)
    addr = s(masterDir=D.OUT, width=ADDR_WIDTH)
    din = s(masterDir=D.OUT, width=DATA_WIDTH)
    dout = s(masterDir=D.IN, width=DATA_WIDTH)
    # en = s("_en", masterDir=D.OUT)
    we = s(masterDir=D.OUT)   
    
class AxiStream(Interface):
    DATA_WIDTH = Param(64)
    last = s(masterDir=D.OUT)
    strb = s(masterDir=D.OUT, width=DATA_WIDTH)
    data = s(masterDir=D.OUT, width=DATA_WIDTH)
    ready = s(masterDir=D.IN)
    valid = s(masterDir=D.OUT)
 

    
allInterfaces = [Ap_clk, BramPort,AxiStream, Ap_hs, Ap_none]
