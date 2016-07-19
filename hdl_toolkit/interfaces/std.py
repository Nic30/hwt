from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.vectorUtils import getWidthExpr
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.interfaces.signalOps import SignalOps
from hdl_toolkit.hdlObjects.types.bits import Bits

D = DIRECTION

class Signal(SignalOps, Interface):
    def __init__(self, masterDir=DIRECTION.OUT, multipliedBy=None,
                   dtype=BIT, isExtern=False, alternativeNames=None,
                   loadConfig=True):
        super().__init__(masterDir=masterDir, multipliedBy=multipliedBy,
             isExtern=isExtern, alternativeNames=alternativeNames,
             loadConfig=loadConfig)
        self._dtype = dtype
        self._setMultipliedBy(multipliedBy, updateTypes=True)
    
    def _injectMultiplerToDtype(self):
        t = self._dtype
        factor = self._multipliedBy
        if t == BIT:
            newT = vecT(factor)
        elif isinstance(t, Bits):
            w = getWidthExpr(t)
            if isinstance(w, RtlSignalBase):
                # bouth Param or factor Value
                newW = w * factor
            elif isinstance(factor, RtlSignalBase):
                # w is Value
                newW = factor * w
            else:
                # bouth Value
                newW = w.clone()
                newW.val *= factor.val
            newT = vecT(newW)
        else:
            raise NotImplementedError("type:%s" % (repr(t)))
        self._dtype = newT
            
    def _setMultipliedBy(self, factor, updateTypes=True):
        if type(self._multipliedBy) == type(factor) and self._multipliedBy == factor:
            pass
        else:
            self._multipliedBy = factor
            if updateTypes and factor is not None:
                self._injectMultiplerToDtype()


class Clk(Signal):
    _alternativeNames = ['ap_clk', 'aclk', 'clk', 'clock']


class Rst(Signal):
    _alternativeNames = ['ap_rst', 'areset', 'reset', 'rst']


class Rst_n(Signal):
    _alternativeNames = ['ap_rst_n', 'aresetn', 'resetn', 'rstn', 'rst_n' ]
    def _signalsForInterface(self, context, prefix='', typeTransform=lambda x:x):
        sigs = Signal._signalsForInterface(self, context, prefix, 
                                            typeTransform=typeTransform)
        for s in sigs:
            s.negated = True
        return sigs


class VldSynced(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        self.data = s(dtype=vecT(self.DATA_WIDTH))
        self.vld = s(alternativeNames=['valid'])


class RdSynced(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)
    
    def _declr(self):
        self.data = s(dtype=vecT(self.DATA_WIDTH))
        self.rd = s(masterDir=D.IN, alternativeNames=['ready'])
    

class Handshaked(VldSynced):
    def _declr(self):
        super()._declr()
        self.rd = s(masterDir=D.IN, alternativeNames=['ready'])

class HandshakeSync(Interface):
    def _declr(self):
        self.vld = s(alternativeNames=['valid'])
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
        assert isinstance(bramPort, BramPort_withoutClk)
        assert isinstance(clk, Clk)
        self = cls()
        rp = self._replaceParam
        def setIntf(name, intf):
            setattr(self, name, intf)
            self._interfaces.append(intf)
        
        rp("ADDR_WIDTH" , bramPort.ADDR_WIDTH)  
        rp("DATA_WIDTH" , bramPort.DATA_WIDTH)  

        self._interfaces = []
        for iName in ["addr", "din", "dout", "en", "we" ]:
            intf = getattr(bramPort, iName)
            setIntf(iName, intf)
        setIntf("clk", clk)
        
        return self   
        

class FifoWriter(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        
    def _declr(self):
        self.en = s()
        self.wait = s(masterDir=DIRECTION.IN)
        self.data = s(dtype=vecT(self.DATA_WIDTH), alternativeNames=[''])


class FifoReader(FifoWriter):
    def _declr(self):
        super()._declr()
        self.en._masterDir = DIRECTION.IN
        self.wait._masterDir = DIRECTION.OUT


class SPI(Interface):
    def _declr(self):
        self.clk = Clk()
        self.mosi = s()
        self.miso = s(masterDir=D.IN)
        self.ss = s()


s = Signal
  
# class RGMII_channel(Interface):
#    def _config(self):
#        self.DATA_WIDTH = 4
#        
#    def _declr(self):
#        self.c = s()
#        self.d = s(dtype=vecT(self.DATA_WIDTH))
#        self.x_ctl = s()
    
