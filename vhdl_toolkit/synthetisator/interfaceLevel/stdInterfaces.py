from vhdl_toolkit.synthetisator.interfaceLevel.interface import  Interface
from vhdl_toolkit.types import DIRECTION

D = DIRECTION


class Ap_none(Interface):
    def __init__(self, *destinations, masterDir=D.OUT, width=1, src=None, isExtern=False):
        Interface.__init__(self, *destinations, src=src, isExtern=isExtern)
        self._width = width
        self._masterDir = masterDir
        
s= Ap_none        

class Ap_clk(Interface):
    ap_clk = s(masterDir=D.OUT, width=1)
        
class Ap_hs(Interface):
    DATA_WIDTH = 64
    data = s(masterDir=D.OUT, width=DATA_WIDTH)
    rd = s(masterDir=D.IN, width=1)
    vld = s(masterDir=D.OUT, width=1)

class BramPort(Interface):
    ADDR_WIDTH = 32
    DATA_WIDTH = 64 
    clk = s(masterDir=D.OUT, width=1)
    addr = s(masterDir=D.OUT, width=ADDR_WIDTH)
    din = s(masterDir=D.OUT, width=DATA_WIDTH)
    dout = s(masterDir=D.IN, width=DATA_WIDTH)
    # en = s("_en", masterDir=D.OUT, width=1)
    we = s(masterDir=D.OUT, width=1)   
    
class AxiStream(Ap_hs):
    last = s(masterDir=D.OUT, width=1)
    strb = s(masterDir=D.OUT, width=Ap_hs.DATA_WIDTH)

    
 

    
allInterfaces = [Ap_clk, BramPort,AxiStream, Ap_hs, Ap_none]
