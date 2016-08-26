from cli_toolkit.ip_packager.interfaces.intfConfig import IntfConfig 


def AxiMap(prefix, listOfNames, d=None):
    if d is None:
        d = {}
    for n in listOfNames:
        d[n] = (prefix + n).upper()
    return d

   
        
class IP_AXIStream(IntfConfig):
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
        
class IP_AXILite(IntfConfig):
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

