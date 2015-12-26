from vhdl_toolkit.synthetisator.interfaceLevel.interface import  Interface
from vhdl_toolkit.types import DIRECTION
from vhdl_toolkit.synthetisator.param import Param

D = DIRECTION


class Ap_none(Interface):
    def __init__(self, *destinations, masterDir=D.OUT, width=1, src=None,\
                  isExtern=False, alternativeNames=None):
        Interface.__init__(self, *destinations, masterDir=masterDir, src=src, \
                           isExtern=isExtern, alternativeNames=alternativeNames)
        self._width = width

        
s = Ap_none        

class Ap_clk(Ap_none):
    pass

class Ap_rst_n(Ap_none):
    pass
    
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
    strb = s(masterDir=D.OUT, width=DATA_WIDTH.get() // 8)  # [TODO] Param needs something like expr, this does not work
    data = s(masterDir=D.OUT, width=DATA_WIDTH)
    ready = s(masterDir=D.IN)
    valid = s(masterDir=D.OUT)



class AxiLite_addr(Interface):
    ADDR_WIDTH = Param(32)
    addr = s(masterDir=D.OUT, width=ADDR_WIDTH, alternativeNames=['addr_v'])
    ready = s(masterDir=D.IN)
    valid = s(masterDir=D.OUT)

class AxiLite_r(Interface):
    DATA_WIDTH = Param(64)
    data = s(masterDir=D.IN, width=DATA_WIDTH, alternativeNames=['data_v'])
    resp = s(masterDir=D.IN, width=2, alternativeNames=['resp_v'])
    ready = s(masterDir=D.OUT)
    valid = s(masterDir=D.IN)

class AxiLite_w(Interface):
    DATA_WIDTH = Param(64)
    data = s(masterDir=D.OUT, width=DATA_WIDTH, alternativeNames=['data_v'])
    strb = s(masterDir=D.OUT, width=DATA_WIDTH.get() // 8, alternativeNames=['strb_v'])  # [TODO] Param needs something like expr, this does not work
    ready = s(masterDir=D.IN)
    valid = s(masterDir=D.OUT)
    
class AxiLite_b(Interface):
    resp = s(masterDir=D.IN, width=2, alternativeNames=['resp_v'])
    ready = s(masterDir=D.OUT)
    valid = s(masterDir=D.IN)

def inherieitAllParams(cls):
    cls._builded()
    for _, intf in cls._subInterfaces.items():
        for paramName, param in cls._params.items():
            if hasattr(intf, paramName):
                p = getattr(intf, paramName)
                p.inherieit(param) 
    
class AxiLite(Interface):
    ADDR_WIDTH = Param(32)
    DATA_WIDTH = Param(64)
    aw = AxiLite_addr()
    ar = AxiLite_addr()
    w = AxiLite_w()
    r = AxiLite_r()
    b = AxiLite_b()
inherieitAllParams(AxiLite)
    
    
allInterfaces = [
                 AxiLite,
                 Ap_clk, Ap_rst_n, 
                 BramPort, AxiStream, Ap_hs, Ap_none
                 ]
