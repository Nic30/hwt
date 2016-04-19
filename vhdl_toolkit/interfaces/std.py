from vhdl_toolkit.synthetisator.interfaceLevel.interface import  Interface
from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.typeDefs import BIT, Std_logic_vector_contrained
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT
from vhdl_toolkit.hdlObjects.vectorUtils import getWidthExpr


D = DIRECTION

class Ap_none(Interface):
    def __init__(self, masterDir=DIRECTION.OUT, multipliedBy=None,
                   dtype=BIT, isExtern=False, alternativeNames=None,
                   loadConfig=True):
        #self._multipliedBy = None
        super().__init__(masterDir=masterDir, multipliedBy=multipliedBy,
             isExtern=isExtern, alternativeNames=alternativeNames, 
             loadConfig=loadConfig)
        self._dtype = dtype
        self._setMultipliedBy(multipliedBy, updateTypes=True)
        # make empty containers
#        self._interfaces = []
#        self._params = []
    
    def _injectMultiplerToDtype(self):
        t = self._dtype
        factor = self._multipliedBy
        if t == BIT:
            newT = vecT(factor)
        elif isinstance(t, Std_logic_vector_contrained):
            w = getWidthExpr(t)
            newT = vecT(w.opMul(factor))
        else:
            raise NotImplementedError("type:%s" % (repr(t)))
        self._dtype = newT
            
    def _setMultipliedBy(self, factor, updateTypes=True):
        if type(self._multipliedBy) == type(factor) and self._multipliedBy == factor:
            pass
        else:
            self._multipliedBy = factor
            if updateTypes and factor is not None:
                self.injectMultiplerToDtype()

s = Ap_none
     

class Ap_clk(Ap_none):
    _alternativeNames = ['ap_clk', 'aclk', 'clk', 'clock']

class Ap_rst(Ap_none):
    _alternativeNames = ['ap_rst', 'areset', 'reset', 'rst']

class Ap_rst_n(Ap_none):
    _alternativeNames = ['ap_rst_n', 'aresetn', 'resetn', 'rstn' ]

class Ap_vld(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        self.data = s(dtype=vecT(self.DATA_WIDTH))
        self.vld = s(alternativeNames=['valid'])

class Ap_hs(Ap_vld):
    def _declr(self):
        self.rd = s(masterDir=D.IN, alternativeNames=['ready'])

class BramPort_withoutClk(Interface):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64) 
        
    def _declr(self):
        self.addr = s(dtype=vecT(self.ADDR_WIDTH), alternativeNames=['addr_v'])
        self.din = s(dtype=vecT(self.DATA_WIDTH), alternativeNames=['din_v'])
        self.dout = s(masterDir=D.IN, dtype=vecT(self.DATA_WIDTH), alternativeNames=['dout_v'])
        self.en = s()
        self.we = s()   

class BramPort(BramPort_withoutClk):
    def _declr(self):
        super()._declr()
        self.clk = s(masterDir=D.OUT)
    
    @classmethod
    def fromBramPort_withoutClk(cls, bramPort, clk):
        raise NotImplementedError("[TODO]:update")
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
    def _declr(self):
        self.clk = Ap_clk()
        self.mosi = s()
        self.miso = s(masterDir=D.IN)
        self.ss = s()
  
#class RGMII_channel(Interface):
#    def _config(self):
#        self.DATA_WIDTH = 4
#        
#    def _declr(self):
#        self.c = s()
#        self.d = s(dtype=vecT(self.DATA_WIDTH))
#        self.x_ctl = s()
    
