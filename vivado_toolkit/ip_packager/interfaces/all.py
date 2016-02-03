from vhdl_toolkit.types import DIRECTION
from vivado_toolkit.ip_packager.others import Parameter
from python_toolkit.arrayQuery import single, where
from vhdl_toolkit.synthetisator.interfaceLevel import interfaces
import vhdl_toolkit.synthetisator.interfaceLevel.interfaces.std
import vhdl_toolkit.synthetisator.interfaceLevel.interfaces.amba

from vivado_toolkit.ip_packager.helpers import mkSpiElm, spi_ns_prefix
         
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
    def findPort(self, logName):
        logName = logName.lower()
        p = single(self.port, lambda x : x.logName.lower() == logName)
        return p

    def addSimpleParam(self, thisIf, name, value):
        p_aw = Parameter()
        p_aw.name = name
        p_aw.value.resolve = "immediate"
        p_aw.value.id = "BUSIFPARAM_VALUE." + thisIf.name.upper() + "." + name.upper()
        p_aw.value.text = value
        thisIf.parameters.append(p_aw)
    
    def postProcess(self, component, entity, allInterfaces, thisIfPrefix):
        pass 

def AxiMap(prefix, listOfNames, d=None):
    if d is None:
        d = {}
    for n in listOfNames:
        d[n] = (prefix + n).upper()

class BlockRamPort(IfConfig):
    def __init__(self):
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



class Handshake(IfConfig):
    def __init__(self):
        self.name = "handshake"
        self.version = "1.0"
        self.vendor = "nic" 
        self.library = "user"
        self.port = {'rd': "ap_vld",
                     'rd': "ap_ack",
                     "data":"data"   }
        
class Ap_clk(IfConfig):
    def __init__(self):
        self.name = "clock"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        self.map = 'CLK'
            
    def postProcess(self, component, entity, allInterfaces, thisIf):
            rst = list(where(allInterfaces, lambda intf: isinstance(intf, interfaces.std.Ap_rst_n) 
                                                        or isinstance(intf, interfaces.std.Ap_rst)))
            if len(rst) > 0:
                self.addSimpleParam(thisIf, "ASSOCIATED_RESET", rst[0]._portMaps['rst'])  # getResetPortName
            elif len(rst) > 1:
                raise Exception("Dont know how to work with multiple resets")
            
            intfs = where(allInterfaces, lambda intf: intf != rst and intf != thisIf)
            self.addSimpleParam(thisIf, "ASSOCIATED_BUSIF", ":".join(map(lambda intf: intf.name, intfs)))
            self.addSimpleParam(thisIf, "FREQ_HZ", str(DEFAULT_CLOCK))

class Ap_rst(IfConfig):
    def __init__(self):
        self.name = "reset"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        self.map = "rst"
        
    def postProcess(self, component, entity, allInterfaces, thisIf):
        self.addSimpleParam(thisIf, "POLARITY", "ACTIVE_HIGH")

class Ap_rst_n(IfConfig):
    def __init__(self):
        self.name = "reset"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "signal"
        self.map = "rst"
        
    def postProcess(self, component, entity, allInterfaces, thisIf):
        self.addSimpleParam(thisIf, "POLARITY", "ACTIVE_LOW")
        
class AXIStream(IfConfig):
    def __init__(self):
        self.name = "axis"
        self.version = "1.0"
        self.vendor = "xilinx.com" 
        self.library = "interface"
        self.map = {'data':"TDATA",
                     'last':"TLAST",
                     'valid':"TVALID",
                     'strb':"TSTRB",
                     'ready':"TREADY"
                     }
        
class AXILite(IfConfig):
    def __init__(self):
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
        thisIf.endianness = "little"
        self.addSimpleParam(thisIf, "ADDR_WIDTH", thisIf.aw.addr.getwidth())
        self.addSimpleParam(thisIf, "DATA_WIDTH", thisIf.w.data.getwidth())
        self.addSimpleParam(thisIf, "PROTOCOL", "AXI4LITE")
        self.addSimpleParam(thisIf, "READ_WRITE_MODE", "READ_WRITE")

# class Axi(AXILite):
#    def __init__(self, ID_WIDTH=0, A_WIDTH=0, D_WIDTH=0):
#        super().__init__(A_WIDTH, D_WIDTH)
#        self.ID_WIDTH = ID_WIDTH
#        self.port += [
#                      c("ARID", masterDir=D.OUT, width=ID_WIDTH),
#                      c("ARBURST", masterDir=D.OUT, width=2),
#                      c("ARCACHE", masterDir=D.OUT, width=4),
#                      c("ARLEN", masterDir=D.OUT, width=8),
#                      c("ARLOCK", masterDir=D.OUT, width=2),
#                      c("ARPROT", masterDir=D.OUT, width=3),
#                      c("ARSIZE", masterDir=D.OUT, width=3),
#                      c("ARQOS", masterDir=D.OUT, width=4),
#                      
#                      c("BID", masterDir=D.IN, width=ID_WIDTH),
#                      
#                      c("AWID", masterDir=D.OUT, width=ID_WIDTH),
#                      c("AWBURST", masterDir=D.OUT, width=2),
#                      c("AWCACHE", masterDir=D.OUT, width=4),
#                      c("AWLEN", masterDir=D.OUT, width=8),
#                      c("AWLOCK", masterDir=D.OUT, width=2),
#                      c("AWPROT", masterDir=D.OUT, width=3),
#                      c("AWSIZE", masterDir=D.OUT, width=3),
#                      c("AWQOS", masterDir=D.OUT, width=4),
#                      
#                      
#                      c("RID", masterDir=D.IN, width=ID_WIDTH),
#                      c("RLAST", masterDir=D.IN, width=1),
#                      
#                      c("WID", masterDir=D.OUT, width=ID_WIDTH),
#                      c("WLAST", masterDir=D.OUT, width=1),
#                      ]
#                     
#    def postProcess(self, component, entity, allInterfaces, thisIf):
#        thisIf.endianness = "little"
#        pw_param = lambda name, portLogName : self.addSimpleParam(thisIf, name, self.getPortWidth(component, thisIf , portLogName))
#        param = lambda name, val :  self.addSimpleParam(thisIf, name, val)
#        pw_param("ADDR_WIDTH", "AWADDR")
#        param("MAX_BURST_LENGTH", str(256))
#        param("NUM_READ_OUTSTANDING", str(5))
#        param("NUM_WRITE_OUTSTANDING", str(5))
#        param("PROTOCOL", "AXI4")
#        param("READ_WRITE_MODE", "READ_WRITE")
#        param("SUPPORTS_NARROW_BURST", str(0))
      
allBusInterfaces = { interfaces.std.BramPort : BlockRamPort,
                     interfaces.amba.AxiStream : AXIStream
                    }
