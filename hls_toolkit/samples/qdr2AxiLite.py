from myhdl import always_seq, always_comb, Signal, modbv, ResetSignal, enum
from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.interfaces.std import s, D
from hdl_toolkit.interfaces.amba import AxiLite_b, AxiLite_addr, AxiLite_r, AxiLite_w, RESP_OKAY
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.hdlObjects.typeShortcuts import hInt, vecT
from hdl_toolkit.hdlObjects.typeDefs import BIT
from hls_toolkit.myhdlSynthesiser import toMyHdlInterface, convert

class QdrAppPort0(Interface):
    ADDR_WIDTH = Param(hInt(18))
    DATA_WIDTH = Param(hInt(144))
    
    wr_cmd0 = s(dtype=BIT)
    wr_addr0 = s(dtype=vecT(ADDR_WIDTH))
    wr_data0 = s(dtype=vecT(DATA_WIDTH))
    wr_bw_n0 = s(dtype=vecT(DATA_WIDTH.opDiv(hInt(8))))
    
    rd_cmd0 = s(dtype=BIT)
    rd_addr0 = s(dtype=vecT(ADDR_WIDTH))
    rd_valid0 = s(masterDir=D.IN, dtype=BIT)
    rd_data0 = s(masterDir=D.IN, dtype=vecT(DATA_WIDTH))
    

def qdr2AxiLite(clk, rst, qdr, axiAr, axiR, axiAw, axiW, axiB,):
    """
    For simplicity address has to be aligned to qdr address granularity
    
    unit was implemented for 
    axilite - 32b addr, 32b data  
    qdr - 18b addr, 36b data
   
    """
    axiAW = 32
    axiDw = 32
    qdrAW = 18
    qdrDW = 144
    
    rDataReg = Signal(modbv(0)[qdrDW:])
    wAddrReg = Signal(modbv(0)[axiAW:])
    
    t_rFsm = enum('RREADY', 'RRESP')
    t_wFsm = enum('WREADY', 'WCATCH', "BRESP")
    
    rSt = Signal(t_rFsm.RREADY)
    rSt_next = Signal(t_rFsm.RREADY)
    
    wSt = Signal(t_wFsm.WREADY)
    wSt_next = Signal(t_wFsm.WREADY)
    
    @always_comb
    def rResponseToAxiRead():
        axiR.data.next = rDataReg
        axiR.resp.next = RESP_OKAY
        axiR.valid.next = rSt == t_rFsm.RRESP
    
  
    @always_seq(clk.posedge, reset=rst)
    def axiReadDataToReg():
        if qdr.rd_valid0:
            rDataReg.next = qdr.rd_data0
        else:
            rDataReg.next = rDataReg
            
    @always_comb
    def axiReadAddr():
        qdr.rd_addr0.next = axiAr.addr[:axiAW - 5]  # cut last 5 bits
        if rSt == t_rFsm.RREADY:
            axiAr.ready.next = True
            qdr.rd_cmd0.next = axiAr.valid
        else:
            qdr.rd_cmd0.next = False
            axiAr.ready.next = False

    @always_comb
    def rFsmTransitions():
        if rSt == t_rFsm.RREADY and axiAr.valid:
            rSt_next.next = t_rFsm.RRESP
        elif rSt == t_rFsm.RRESP and axiR.ready:
            rSt_next.next = t_rFsm.RREADY
        else:
            rSt_next.next = rSt

    @always_comb
    def axiWriteAddrComb():
        if wSt == t_wFsm.WREADY:
            axiAw.ready.next = True
        else:
            axiAw.ready.next = False
    
    @always_seq(clk.posedge, reset=rst)
    def axiWriteAddrRegProc():
        if wSt == t_wFsm.WREADY:
            wAddrReg.next = axiAw.addr[:axiAW - 5]  # cut last 5 bits
        else:
            wAddrReg.next = wAddrReg
    
    
    @always_comb
    def axiWriteData():
        qdr.wr_addr0.next = wAddrReg
        qdr.wr_data0.next = axiW.data
        qdr.wr_bw_n0.next = axiW.strb 
        if wSt == t_wFsm.WCATCH:
            axiW.ready.next = True
            qdr.wr_cmd0.next = axiW.valid
        else:
            axiW.ready.next = False
            qdr.wr_cmd0.next = False
    
    @always_comb
    def axiWriteRespB():
        axiB.resp.next = RESP_OKAY
        axiB.valid.next = wSt == t_wFsm.BRESP
                    
    @always_comb
    def wFsmTransitions():
        if wSt == t_wFsm.WREADY and axiAw.valid:
            wSt_next.next = t_wFsm.WCATCH
        elif wSt == t_wFsm.WCATCH and axiW.valid:
            wSt_next.next = t_wFsm.BRESP
        elif wSt == t_wFsm.BRESP and axiB.ready:
            wSt_next.next = t_wFsm.WREADY
        else:
            wSt_next.next = wSt          
                
    @always_seq(clk.posedge, reset=rst) 
    def fsmStShift():
        rSt.next = rSt_next
        wSt.next = wSt_next
 
        
        
    return [rResponseToAxiRead, axiReadDataToReg, axiReadAddr, rFsmTransitions
            , axiWriteAddrComb, axiWriteAddrRegProc, axiWriteData, wFsmTransitions,
            axiWriteRespB,
             fsmStShift]
    
if __name__ == "__main__":
    clk = Signal(bool(0))
    rst = ResetSignal(0, active=0, async=False)
    qdr = toMyHdlInterface(QdrAppPort0())
    axiAr = toMyHdlInterface(AxiLite_addr())
    axiAw = toMyHdlInterface(AxiLite_addr())
    axiR = toMyHdlInterface(AxiLite_r())
    axiW = toMyHdlInterface(AxiLite_w())
    axiB = toMyHdlInterface(AxiLite_b())
    
    convert(qdr2AxiLite, clk, rst, qdr, axiAr, axiR, axiAw, axiW, axiB)


