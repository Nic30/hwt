from myhdl import always_seq, always_comb, Signal, modbv, ResetSignal, enum
from vhdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from vhdl_toolkit.interfaces.std import s, D
from vhdl_toolkit.interfaces.amba import AxiLite_b, AxiLite_addr, AxiLite_r, AxiLite_w, RESP_OKAY
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt, vecT
from vhdl_toolkit.hdlObjects.typeDefs import BIT
from hls_toolkit.myhdlSynthesiser import toMyHdlInterface, convert

class ft245syncIntf(Interface):
    DATA_WIDTH = Param(hInt(8))
    
    dataIn  = s(masterDir=D.IN, dtype=vecT(DATA_WIDTH)) #Data writen from controller
    dataOut = s(dtype=vecT(DATA_WIDTH)) #Data read from controller 
    rw = s(dtype=BIT) #data direction 0 read, 1 write
    busy = s(masterDir=D.IN, dtype=BIT) # busy flag
    strobe = s(masterDir=D.IN, dtype=BIT) #strobe of RW flag


LEN_W = 7
ADDR_W = 32
WORD_W = 32

#class ft245AxiFrame():
#    rw = Signal(bool())
#    len = Signal(modbv(0)[LEN_W:])
#    addr = Signal(modbv(0)[ADDR_W:])
#    data = Signal(modbv(0)[WORD_W*LEN_W:])

t_stPackReader = enum("RD_LEN", "RD_ADDR", "RD_DATA", "SUSPENDED")
t_stDataWLoader = enum("")
t_state = enum("IDLE", 
               "AXI_AR", "AXI_R",
               "AXI_AW", "AXI_W", "AXI_WAIT_B")
def ft245ToAxi(clk, rst, ft245sIf, axiAr, axiR, axiAw, axiW, axiB):
    pReaderSt = Signal(t_stPackReader.RD_LEN)
    pReaderSt_next = Signal(t_stPackReader.RD_LEN)

    rw = Signal(bool())                   
    len = Signal(modbv(0)[LEN_W:])        
    addr = Signal(modbv(0)[ADDR_W:])      

    rw_next = Signal(bool())                   
    len_next = Signal(modbv(0)[LEN_W:])        
    addr_next = Signal(modbv(0)[ADDR_W:])      

    newPacket = Signal(bool())
    
    addrLdIndexer = Signal(modbv(0)[ADDR_W//8:])
    addrLdIndexer_next = Signal(modbv(0)[ADDR_W//8:])    
    
    addrLdIndexer = Signal(modbv(0)[ADDR_W//8:])
    
    lenRem = Signal(modbv(0)[LEN_W:])

    
    @always_comb
    def packetLoader():
        rw_next.next =   rw
        len_next.next =  len
        addr_next.next = addr
        
        if pReaderSt == t_stPackReader.RD_LEN:
            rw_next.next =  ft245sIf.dataIn[LEN_W]
            len_next.next = ft245sIf.dataIn
        elif pReaderSt == t_stPackReader.RD_ADDR:
            addr_next.next[addrLdIndexer*8:8] = ft245sIf.dataIn
        elif pReaderSt == t_stPackReader.RD_DATA:
            pass
        else:
            pass
        
    @always_seq(clk.posedge, reset=rst)        
    def addrLdIndexer_incrementer():
        if pReaderSt == t_stPackReader.RD_LEN:
            addrLdIndexer_next.next = 0
        elif pReaderSt == t_stPackReader.RD_ADDR:
            if not ft245sIf.busy:
                addrLdIndexer_next.next = addrLdIndexer + 1
        else:
            addrLdIndexer_next.next = addrLdIndexer
    
    @always_comb
    def packetLoaderStateChange():
        pReaderSt_next.next = pReaderSt
        
        if not ft245sIf.busy:
            if pReaderSt == t_stPackReader.RD_LEN:
                pReaderSt_next.next = t_stPackReader.RD_ADDR
            elif pReaderSt == t_stPackReader.RD_ADDR:
                if addrLdIndexer == 3:
                    pReaderSt_next.next = t_stPackReader.RD_DATA
            elif pReaderSt == t_stPackReader.RD_DATA:
                if lenRem ==0:
                    pReaderSt_next.next = t_stPackReader.SUSPENDED
            elif pReaderSt == t_stPackReader.SUSPENDED:
                if newPacket:
                    pReaderSt_next.next = t_stPackReader.RD_LEN
          
            
    
    @always_seq(clk.posedge, reset=rst)
    def stateShift():
        pReaderSt.next = pReaderSt_next
        
        rw.next =   rw_next
        len.next =  len_next
        addr.next = addr_next

   
   
    return [packetLoader, 
            addrLdIndexer_incrementer,
            packetLoaderStateChange,
            stateShift
            ]     

if __name__ == "__main__":
    clk = Signal(bool(0))
    rst = ResetSignal(0, active=0, async=False)
    ft245sIf = toMyHdlInterface(ft245syncIntf())
    axiAr = toMyHdlInterface(AxiLite_addr())
    axiAw = toMyHdlInterface(AxiLite_addr())
    axiR = toMyHdlInterface(AxiLite_r())
    axiW = toMyHdlInterface(AxiLite_w())
    axiB = toMyHdlInterface(AxiLite_b())
    
    convert(ft245ToAxi, clk, rst, ft245sIf, axiAr, axiR, axiAw, axiW, axiB)


