from hdl_toolkit.synthetisator.interfaceLevel.interface import  Interface
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.interfaces.std import s, D
from hdl_toolkit.hdlObjects.typeShortcuts import vecT


BURST_FIXED = 0b00
BURST_INCR = 0b01
BURST_WRAP = 0b10

BYTES_IN_TRANS_1 = 0b000
BYTES_IN_TRANS_2 = 0b001
BYTES_IN_TRANS_4 = 0b010
BYTES_IN_TRANS_8 = 0b011
BYTES_IN_TRANS_16 = 0b100
BYTES_IN_TRANS_32 = 0b101
BYTES_IN_TRANS_64 = 0b110
BYTES_IN_TRANS_128 = 0b111

CACHE_DEFAULT = 3
PROT_DEFAULT = 0
QOS_DEFAULT = 0
LOCK_DEFAULT = 0
RESP_OKAY = 0
RESP_EXOKAY = 1
RESP_SLVERR = 2
RESP_DECERR = 3

# http://www.xilinx.com/support/documentation/ip_documentation/ug761_axi_reference_guide.pdf
    
class AxiStream_withoutSTRB(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)

    def _declr(self):
        self.last = s(masterDir=D.OUT, alternativeNames=['tlast' ])
        self.data = s(masterDir=D.OUT, dtype=vecT(self.DATA_WIDTH), alternativeNames=['tdata' ])
        self.ready = s(masterDir=D.IN, alternativeNames=['tready' ])
        self.valid = s(masterDir=D.OUT, alternativeNames=['tvalid' ])

class AxiStream(AxiStream_withoutSTRB):
    def _declr(self):
        super(AxiStream, self)._declr()
        self.strb = s(masterDir=D.OUT,
                 dtype=vecT(self.DATA_WIDTH // 8),
                 alternativeNames=['tstrb', 'keep', 'tkeep' ])
        
class Axi_user(Interface):
    def _config(self):
        self.USER_WIDTH = Param(0)
        
    def _declr(self):
        self.user = s(masterDir=D.OUT,
                 dtype=vecT(self.USER_WIDTH),
                 alternativeNames=['tuser'])

class AxiStream_withUserAndNoStrb(AxiStream_withoutSTRB, Axi_user):
    def _config(self):
        AxiStream_withoutSTRB._config(self)
        Axi_user._config(self)
    
    def _declr(self):
        AxiStream_withoutSTRB._declr(self)
        Axi_user._declr(self)
        
    
class AxiStream_withUserAndStrb(AxiStream, Axi_user):
    def _config(self):
        AxiStream._config(self)
        Axi_user._config(self)
    
    def _declr(self):
        AxiStream._declr(self)
        Axi_user._declr(self)
        
            
class AxiLite_addr(Interface):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        
    def _declr(self):
        self.addr = s(masterDir=D.OUT, dtype=vecT(self.ADDR_WIDTH), alternativeNames=['addr_v'])
        self.ready = s(masterDir=D.IN)
        self.valid = s(masterDir=D.OUT)

class AxiLite_r(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)
        
    def _declr(self):
        self.data = s(masterDir=D.IN, dtype=vecT(self.DATA_WIDTH), alternativeNames=['data_v'])
        self.resp = s(masterDir=D.IN, dtype=vecT(2), alternativeNames=['resp_v'])
        self.ready = s(masterDir=D.OUT)
        self.valid = s(masterDir=D.IN)

class AxiLite_w(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(64)
        
    def _declr(self):
        self.data = s(masterDir=D.OUT, dtype=vecT(self.DATA_WIDTH), alternativeNames=['data_v'])
        self.strb = s(masterDir=D.OUT,
                      dtype=vecT(self.DATA_WIDTH // 8), alternativeNames=['strb_v'])
        self.ready = s(masterDir=D.IN)
        self.valid = s(masterDir=D.OUT)
        
    
class AxiLite_b(Interface):
    def _declr(self):
        self.resp = s(masterDir=D.IN, dtype=vecT(2), alternativeNames=['resp_v'])
        self.ready = s(masterDir=D.OUT)
        self.valid = s(masterDir=D.IN)

class AxiLite(Interface):
    def _config(self):
        self.ADDR_WIDTH = Param(32)
        self.DATA_WIDTH = Param(64)
        
    def _declr(self):
        self.aw = AxiLite_addr()
        self.ar = AxiLite_addr()
        self.w = AxiLite_w()
        self.r = AxiLite_r()
        self.b = AxiLite_b()
        self._shareAllParams()
        
class AxiLite_addr_xil(AxiLite_addr):
    _NAME_SEPARATOR = ''
class AxiLite_r_xil(AxiLite_r):
    _NAME_SEPARATOR = ''
class AxiLite_w_xil(AxiLite_w):
    _NAME_SEPARATOR = ''
class AxiLite_b_xil(AxiLite_b):
    _NAME_SEPARATOR = ''
    
class AxiLite_xil(AxiLite):
    def _declr(self):
        self.aw = AxiLite_addr_xil()
        self.ar = AxiLite_addr_xil()
        self.w = AxiLite_w_xil()
        self.r = AxiLite_r_xil()
        self.b = AxiLite_b_xil()   
        self._shareAllParams()
        
class Axi4_addr(AxiLite_addr):
    def _config(self):
        super(Axi4_addr, self)._config()
        self.ID_WIDTH = Param(3)
    
    def _declr(self):
        super(Axi4_addr, self)._declr()
        self.id = s(masterDir=D.OUT, dtype=vecT(self.ID_WIDTH), alternativeNames=['id_v'])
        self.burst = s(masterDir=D.OUT, dtype=vecT(2), alternativeNames=['burst_v'])
        self.cache = s(masterDir=D.OUT, dtype=vecT(4), alternativeNames=['cache_v'])
        self.len = s(masterDir=D.OUT, dtype=vecT(8), alternativeNames=['len_v'])
        self.lock = s(masterDir=D.OUT, dtype=vecT(1), alternativeNames=['lock_v'])
        self.prot = s(masterDir=D.OUT, dtype=vecT(3), alternativeNames=['prot_v'])
        self.size = s(masterDir=D.OUT, dtype=vecT(3), alternativeNames=['size_v'])
        self.qos = s(masterDir=D.OUT, dtype=vecT(4), alternativeNames=['qos_v'])


class Axi4_r(AxiLite_r):
    def _config(self):
        super(Axi4_r, self)._config()
        self.ID_WIDTH = Param(3)
    
    def _declr(self):
        super(Axi4_r, self)._declr()
        self.id = s(masterDir=D.IN, dtype=vecT(self.ID_WIDTH), alternativeNames=['id_v'])
        self.last = s(masterDir=D.IN)

class Axi4_w(AxiLite_w):
    def _config(self):
        super(Axi4_w, self)._config()
        self.ID_WIDTH = Param(3)
    
    def _declr(self):
        super(Axi4_w, self)._declr()
        self.id = s(masterDir=D.OUT, dtype=vecT(self.ID_WIDTH), alternativeNames=['id_v'])
        self.last = s(masterDir=D.OUT)
    
class Axi4_b(AxiLite_b):
    def _config(self):
        super(Axi4_b, self)._config()
        self.ID_WIDTH = Param(3)
    
    def _declr(self):
        super(Axi4_b, self)._declr()
        self.id = s(masterDir=D.IN, dtype=vecT(self.ID_WIDTH), alternativeNames=['id_v'])

class Axi4(AxiLite):
    def _config(self):
        super(Axi4, self)._config()
        self.ID_WIDTH = Param(3)
        
    def _declr(self):
        self.aw = Axi4_addr()
        self.ar = Axi4_addr()
        self.w = Axi4_w()
        self.r = Axi4_r()
        self.b = Axi4_b()
        self._shareAllParams()

class Axi4_addr_xil(Axi4_addr):
    _NAME_SEPARATOR = ''
class Axi4_r_xil(Axi4_r):
    _NAME_SEPARATOR = ''
class Axi4_w_xil(Axi4_w):
    _NAME_SEPARATOR = ''
class Axi4_b_xil(Axi4_b):
    _NAME_SEPARATOR = ''


class Axi4_xil(Axi4):
    def _declr(self):
        self.ar = Axi4_addr_xil()
        self.aw = Axi4_addr_xil()
        self.r = Axi4_r_xil()
        self.w = Axi4_w_xil()
        self.b = Axi4_b_xil()  
        self._shareAllParams()