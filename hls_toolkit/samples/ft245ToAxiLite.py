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
t_MainSt = enum("IDLE", 
               "AXI_AR", "AXI_R",
               "AXI_AW", "AXI_W", "AXI_WAIT_B", "RESPOND_B")

def ft245ToAxi(clk, rst, ft245sIf, axiAr, axiR, axiAw, axiW, axiB):
    pReaderSt    = Signal(t_stPackReader.RD_LEN)
    pReaderSt_next = Signal(t_stPackReader.RD_LEN)
    mainSt       = Signal(t_MainSt.IDLE)
    mainSt_next  = Signal(t_MainSt.IDLE)

    rw = Signal(bool())
    en = Signal(bool())                   
    len = Signal(modbv(0)[LEN_W:])        
    addr = Signal(modbv(0)[ADDR_W:])      

    rw_next = Signal(bool())                   
    len_next = Signal(modbv(0)[LEN_W:])        
    addr_next = Signal(modbv(0)[ADDR_W:])      

    newPacket = Signal(bool())
    
    addrLdIndexer = Signal(modbv(0)[ADDR_W//8:])
    addrLdIndexer_next = Signal(modbv(0)[ADDR_W//8:])    
    
    lenRem = Signal(modbv(0)[LEN_W:])

    axiRespReg = Signal(modbv(0)[2:])
    axiRespRegVld = Signal(bool())
    
    @always_comb
    def mainStNextLogic():
        mainSt_next.next = mainSt
        if mainSt == t_MainSt.IDLE:
            if pReaderSt == t_stPackReader.SUSPENDED:
                if rw:
                    mainSt_next.next = t_MainSt.AXI_AW
                else:
                    mainSt_next.next = t_MainSt.AXI_AR
        elif mainSt == t_MainSt.AXI_AR:
            if axiAr.ready:
                mainSt_next.next = t_MainSt.AXI_R
        elif mainSt == t_MainSt.AXI_R:
            if len == 0:
                mainSt_next.next = t_MainSt.IDLE
        elif mainSt == t_MainSt.AXI_AW:
            if axiAw.ready:
                mainSt_next.next = t_MainSt.AXI_W
        elif mainSt == t_MainSt.AXI_W:
            if len == 0:
                mainSt_next.next = t_MainSt.AXI_WAIT_B
        elif mainSt == t_MainSt.AXI_WAIT_B:
            if axiB.valid:
                mainSt_next.next = t_MainSt.RESPOND_B
        elif mainSt == t_MainSt.RESPOND_B:
            if not ft245sIf.busy:
                mainSt_next.next = t_MainSt.IDLE

    @always_comb
    def axiAr_sender():
        axiAr.addr.next = addr                         
        axiAr.valid.next = mainSt == t_MainSt.AXI_AR
    
    @always_comb
    def axiAw_sender():
        axiAw.addr.next = addr                         
        axiAw.valid.next = mainSt == t_MainSt.AXI_AW
    
    @always_comb
    def axiW_sender():
        axiW.data.next = ft245sIf.dataIn 
        axiW.valid.next = not ft245sIf.busy and mainSt == t_MainSt.AXI_W
    
    @always_comb
    def upstreamDownstream():
        if mainSt == t_MainSt.AXI_R:
            ft245sIf.dataOut.next = axiR.data
            ft245sIf.rw.next = False 
            ft245sIf.strobe.next = axiR.valid
        elif mainSt == t_MainSt.AXI_W:
            ft245sIf.strobe.next = axiW.ready
            ft245sIf.rw.next = True
        elif mainSt == t_MainSt.RESPOND_B:
            ft245sIf.dataOut.next = axiRespReg
            ft245sIf.rw.next = False 
            ft245sIf.strobe.next = True
        else:
            ft245sIf.rw.next =  rw
            ft245sIf.strobe.next = en
    
    @always_comb
    def packetLoader():
        rw_next.next =   rw
        len_next.next =  len
        addr_next.next = addr
        
        if pReaderSt == t_stPackReader.RD_LEN:
            rw_next.next =  ft245sIf.dataIn[LEN_W]
            len_next.next = ft245sIf.dataIn
            en.next = True
        elif pReaderSt == t_stPackReader.RD_ADDR:
            addr_next.next[addrLdIndexer*8:8] = ft245sIf.dataIn
            en.next = True
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
    def dataToft245():
        axiB.ready.next = not axiRespRegVld
        if axiB.valid:
            axiRespReg.next = axiB.resp
            axiRespRegVld.next = True
        elif mainSt != t_MainSt.AXI_WAIT_B:
            axiRespRegVld.next = False 
            
              
            
    
    @always_seq(clk.posedge, reset=rst)
    def stateShift():
        pReaderSt.next = pReaderSt_next
        addrLdIndexer.next = addrLdIndexer_next
        rw.next =   rw_next
        len.next =  len_next
        addr.next = addr_next
        mainSt.next = mainSt_next
   
   
    return [mainStNextLogic,
            upstreamDownstream,
            axiAr_sender,
            axiAw_sender,
            axiW_sender,
            packetLoader, 
            addrLdIndexer_incrementer,
            packetLoaderStateChange,
            dataToft245,
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


