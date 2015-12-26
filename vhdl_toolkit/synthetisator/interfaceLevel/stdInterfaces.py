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


class BramPort_withoutClk(Interface):
    ADDR_WIDTH = Param(32)
    DATA_WIDTH = Param(64) 
    addr = s(masterDir=D.OUT, width=ADDR_WIDTH, alternativeNames=['addr_v'])
    din = s(masterDir=D.OUT, width=DATA_WIDTH, alternativeNames=['din_v'])
    dout = s(masterDir=D.IN, width=DATA_WIDTH, alternativeNames=['dout_v'])
    en = s(masterDir=D.OUT)
    we = s(masterDir=D.OUT)   

class BramPort(BramPort_withoutClk):
    clk = s(masterDir=D.OUT)

    
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

class AxiLite_addr_xil(AxiLite_addr):
    NAME_SEPARATOR = ''

class AxiLite_r_xil(AxiLite_r):
    NAME_SEPARATOR = ''

class AxiLite_w_xil(AxiLite_w):
    NAME_SEPARATOR = ''

class AxiLite_b_xil(AxiLite_b):
    NAME_SEPARATOR = ''
    

class AxiLite_xil(AxiLite):
    aw = AxiLite_addr_xil()
    ar = AxiLite_addr_xil()
    w = AxiLite_w_xil()
    r = AxiLite_r_xil()
    b = AxiLite_b_xil()   
inherieitAllParams(AxiLite)


class Axi4_addr(AxiLite_addr):
    ID_WIDTH = Param(3)
    id = s(masterDir=D.OUT, width = ID_WIDTH, alternativeNames=['id_v'])
    burst = s(masterDir=D.OUT, width=2, alternativeNames=['burst_v'])
    cache = s(masterDir=D.OUT, width=4, alternativeNames=['cache_v'])
    len = s(masterDir=D.OUT, width=7, alternativeNames=['len_v'])
    lock = s(masterDir=D.OUT, width=2, alternativeNames=['lock_v'])
    prot = s(masterDir=D.OUT, width=3, alternativeNames=['prot_v'])
    size = s(masterDir=D.OUT, width=3, alternativeNames=['size_v'])
    qos = s(masterDir=D.OUT, width=4, alternativeNames=['qos_v'])


class Axi4_r(AxiLite_r):
    ID_WIDTH = Param(3)
    id = s(masterDir=D.IN, width=ID_WIDTH, alternativeNames=['id_v'])
    last = s(masterDir=D.IN)

class Axi4_w(AxiLite_w):
    ID_WIDTH = Param(3)
    id = s(masterDir=D.OUT, width=ID_WIDTH, alternativeNames=['id_v'])
    last = s(masterDir=D.OUT)
    
class Axi4_b(AxiLite_b):
    ID_WIDTH = Param(3)
    id = s(masterDir=D.IN, width=ID_WIDTH, alternativeNames=['id_v'])

class Axi4(AxiLite):
    ID_WIDTH = Param(3)
    aw = Axi4_addr()
    ar = Axi4_addr()
    w = Axi4_w()
    r = Axi4_r()
    b = Axi4_b()   
inherieitAllParams(Axi4) 
    
allInterfaces = [Axi4,
                 AxiLite,
                 AxiLite_xil,
                 Ap_clk, Ap_rst_n, 
                 BramPort,BramPort_withoutClk,
                 AxiStream, Ap_hs, Ap_none
                 ]
