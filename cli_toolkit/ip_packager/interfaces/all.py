from python_toolkit.arrayQuery import single, where
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal
from hdl_toolkit import interfaces
import hdl_toolkit.interfaces.std
import hdl_toolkit.interfaces.amba

from hdl_toolkit.synthetisator.param import getParam
from cli_toolkit.ip_packager.otherXmlObjs import Parameter
from cli_toolkit.ip_packager.helpers import mkSpiElm, spi_ns_prefix
from cli_toolkit.ip_packager.exprSerializer import VivadoTclExpressionSerializer

         
DEFAULT_CLOCK = 100000000
D = DIRECTION


class Type():
    __slots__ = ['name', 'version', 'vendor', 'library']
     
    @classmethod 
    def fromElem(cls, elm):
        self = cls()
        for s in ['name', 'version', 'vendor', 'library']:
            setattr(self, s, elm.attrib[spi_ns_prefix + s])
        return self
    
    def asElem(self, elmName):
        e = mkSpiElm(elmName)
        for s in ['name', 'version', 'vendor', 'library']:
            e.attrib[spi_ns_prefix + s] = getattr(self, s)
        return e    
         
class IfConfig(Type):
    def __init__(self):
        self.parameters = []
        self.map = {}
    def findPort(self, logName):
        logName = logName.lower()
        p = single(self.port, lambda x : x.logName.lower() == logName)
        return p

    def addSimpleParam(self, thisIntf, name, value):
        p = Parameter()
        p.name = name
        p.value.resolve = "immediate"
        p.value.id = "BUSIFPARAM_VALUE." + thisIntf._name.upper() + "." + name.upper()
        p.value.text = value
        self.parameters.append(p)
        return p
    
    def addWidthParam(self, thisIntf, name, value):
        p = self.addSimpleParam(thisIntf, "ADDR_WIDTH",
                            VivadoTclExpressionSerializer.asHdl(value.staticEval()))
        if isinstance(value, Signal):
            p.value.resolve = "user" 
        
    def postProcess(self, component, entity, allInterfaces, thisIf):
        pass 

def AxiMap(prefix, listOfNames, d=None):
    if d is None:
        d = {}
    for n in listOfNames:
        d[n] = (prefix + n).upper()
    return d

class IP_BlockRamPort(IfConfig):
    def __init__(self):
        super().__init__()
        self.name = "bram"
        self.version = "1.0"
        self.vendor = "xilinx.com"  
        self.library = "interface" 
        self.map = {'addr':"ADDR",
                    "clk": 'CLK',
                    'din':"DIN",
                    'dout':"DOUT",
                    'en': "EN",
                    'we': "WE",
                    } 

class IP_Handshake(IfConfig):
    def __init__(self):
        super().__init__()
        self.name = "handshake"
        self.version = "1.0"
        self.vendor = "nic" 
        self.library = "user"
        self.map = {'rd': "ap_vld",
                     'rd': "ap_ack",
                     "data":"data"   }
        
class IP_Ap_clk(IfConfig):
    def __init__(self):
        super().__init__()
        self.name = "clock"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        self.map = 'CLK'
            
    def postProcess(self, component, entity, allInterfaces, thisIf):
            rst = list(where(allInterfaces, lambda intf: isinstance(intf, interfaces.std.Ap_rst_n) 
                                                        or isinstance(intf, interfaces.std.Ap_rst)))
            if len(rst) > 0:
                rst = rst[0]
                self.addSimpleParam(thisIf, "ASSOCIATED_RESET", rst._name)  # getResetPortName
                
            elif len(rst) > 1:
                raise Exception("Don't know how to work with multiple resets")
            
            intfs = where(allInterfaces, lambda intf: intf != rst and intf != self)
            self.addSimpleParam(thisIf, "ASSOCIATED_BUSIF", ":".join(map(lambda intf: intf._name, intfs)))
            self.addSimpleParam(thisIf, "FREQ_HZ", str(DEFAULT_CLOCK))

class IP_Ap_rst(IfConfig):
    def __init__(self):
        super().__init__()
        self.name = "reset"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        self.map = "rst"
        
    def postProcess(self, component, entity, allInterfaces, thisIf):
        self.addSimpleParam(thisIf, "POLARITY", "ACTIVE_HIGH")

class IP_Ap_rst_n(IfConfig):
    def __init__(self):
        super().__init__()
        self.name = "reset"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        self.map = "rst"
        
    def postProcess(self, component, entity, allInterfaces, thisIf):
        self.addSimpleParam(thisIf, "POLARITY", "ACTIVE_LOW")
        
class IP_AXIStream(IfConfig):
    def __init__(self):
        super().__init__()
        self.name = "axis"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "interface"
        self.map = {'data':"TDATA",
                     'last':"TLAST",
                     'valid':"TVALID",
                     'strb':"TSTRB",
                     'keep' : "TKEEP",
                     'user' : 'TUSER',
                     'ready':"TREADY"
                     }
        
class IP_AXILite(IfConfig):
    def __init__(self):
        super().__init__()
        self.name = "aximm"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "interface"
        a_sigs = ['addr', 'valid', 'ready']
        self.map = {'aw': AxiMap('aw', a_sigs),
                    'w' : AxiMap('w', ['data', 'strb', 'valid', 'ready']),
                    'ar' : AxiMap('ar', a_sigs),
                     'r' : AxiMap('r', ['data', 'resp', 'valid', 'ready']),
                     'b' : AxiMap('b', ['valid', 'ready', 'resp'])
                     }

        
    def postProcess(self, component, entity, allInterfaces, thisIf):
        self.endianness = "little"
        self.addWidthParam(thisIf, "ADDR_WIDTH", thisIf.ADDR_WIDTH)
        self.addWidthParam(thisIf, "DATA_WIDTH", thisIf.DATA_WIDTH)
        self.addSimpleParam(thisIf, "PROTOCOL", "AXI4LITE")
        self.addSimpleParam(thisIf, "READ_WRITE_MODE", "READ_WRITE")

class IP_Axi4(IP_AXILite):
    def __init__(self,):
        super().__init__()
        a_sigs = ['id', 'burst', 'cache', 'len', 'lock', 'prot', 'size', 'qos']
        AxiMap('ar', a_sigs, self.map['ar'])
        AxiMap('aw', a_sigs, self.map['aw'])
        AxiMap('b', ['id'], self.map['b'])
        AxiMap('r', ['id', 'last'], self.map['r'])
        AxiMap('w', ['id', 'last'], self.map['w'])
                     
    def postProcess(self, component, entity, allInterfaces, thisIf):
        self.endianness = "little"
        param = lambda name, val :  self.addSimpleParam(thisIf, name, str(val))
        param("ADDR_WIDTH", thisIf.aw.addr._dtype.bit_length()) # [TODO] width expression
        param("MAX_BURST_LENGTH", 256)
        param("NUM_READ_OUTSTANDING", 5)
        param("NUM_WRITE_OUTSTANDING", 5)
        param("PROTOCOL", "AXI4")
        param("READ_WRITE_MODE", "READ_WRITE")
        param("SUPPORTS_NARROW_BURST", 0)
      
allBusInterfaces = { interfaces.std.BramPort : IP_BlockRamPort,
                     interfaces.amba.AxiLite : IP_AXILite,
                     interfaces.amba.AxiLite_xil : IP_AXILite,
                     interfaces.amba.AxiStream : IP_AXIStream,
                     
                     interfaces.amba.AxiStream_withoutSTRB :  IP_AXIStream,
                     interfaces.amba.AxiStream_withUserAndNoStrb : IP_AXIStream,
                     interfaces.amba.AxiStream_withUserAndStrb : IP_AXIStream,
                     
                     interfaces.amba.Axi4 : IP_Axi4,
                     interfaces.std.Ap_clk : IP_Ap_clk,
                     interfaces.std.Ap_rst : IP_Ap_rst,
                     interfaces.std.Ap_rst_n : IP_Ap_rst_n
                    }
