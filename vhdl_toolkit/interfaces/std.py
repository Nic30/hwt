from vhdl_toolkit.synthetisator.interfaceLevel.interface import  Interface
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.typeDefs import BIT
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT

D = DIRECTION

class Ap_none(Interface):
    def __init__(self, *destinations, masterDir=DIRECTION.OUT, dtype=BIT, src=None, \
                  isExtern=False, alternativeNames=None):
        Interface.__init__(self, *destinations, masterDir=masterDir, src=src, \
                           isExtern=isExtern, alternativeNames=alternativeNames)
        self._dtype = dtype

s = Ap_none
     

class Ap_clk(Ap_none):
    _alternativeNames = ['ap_clk', 'aclk', 'clk', 'clock']

class Ap_rst(Ap_none):
    _alternativeNames = ['ap_rst', 'areset', 'reset', 'rst']

class Ap_rst_n(Ap_none):
    _alternativeNames = ['ap_rst_n', 'aresetn', 'resetn', 'rstn' ]

class Ap_vld(Interface):
    DATA_WIDTH = Param(64)
    data = s(dtype=vecT(DATA_WIDTH))
    vld = s()

class Ap_hs(Ap_vld):
    rd = s(masterDir=D.IN)

class BramPort_withoutClk(Interface):
    ADDR_WIDTH = Param(32)
    DATA_WIDTH = Param(64) 
    addr = s(dtype=vecT(ADDR_WIDTH), alternativeNames=['addr_v'])
    din = s(dtype=vecT(DATA_WIDTH), alternativeNames=['din_v'])
    dout = s(masterDir=D.IN, dtype=vecT(DATA_WIDTH), alternativeNames=['dout_v'])
    en = s()
    we = s()   

class BramPort(BramPort_withoutClk):
    clk = s(masterDir=D.OUT)
    @classmethod
    def fromBramPort_withoutClk(cls, bramPort, clk):
        assert(isinstance(bramPort, BramPort_withoutClk))
        assert(isinstance(clk, Ap_clk))
        self = cls()
        def overWriteSubIntf(name, intf):
            setattr(self, name, intf)
            self._subInterfaces[name] = intf
        def overWriteParam(name, param):
            setattr(self, name, param)
            self._params[name] = param
                
        overWriteSubIntf("clk", clk)
        
        overWriteParam("ADDR_WIDTH" , bramPort.ADDR_WIDTH)  
        overWriteParam("DATA_WIDTH" , bramPort.DATA_WIDTH)  
        
        overWriteSubIntf("addr", bramPort.addr)     
        overWriteSubIntf("din" , bramPort.din)     
        overWriteSubIntf("dout", bramPort.dout)     
        overWriteSubIntf("en" , bramPort.en)   
        overWriteSubIntf("we" , bramPort.we)
        self._masterDir = bramPort._masterDir
        return self   
        

class SPI(Interface):
    clk = Ap_clk()
    mosi = Ap_none()
    miso = Ap_none(masterDir=D.IN)
    ss = Ap_none()
  
class RGMII_channel(Interface):
    DATA_WIDTH = 4
    c = s()
    d = s(dtype=vecT(DATA_WIDTH))
    x_ctl = s()
    
