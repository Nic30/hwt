from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_clk, Ap_rst_n
from vhdl_toolkit.interfaces.amba import  AxiLite
from vhdl_toolkit.samples.iLvl.axi_basic import AxiLiteBasicSlave
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt

from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls, synthetizeAndSave

class AxiLiteSlaveContainer(Unit):
    slv = AxiLiteBasicSlave()
    
    clk = Ap_clk(slv.S_AXI_ap_clk, isExtern=True)
    rst_n = Ap_rst_n(slv.S_AXI_ap_rst_n, isExtern=True)
    axi = AxiLite(slv.S_AXI, isExtern=True)

    ADDR_WIDTH = axi.ADDR_WIDTH
    DATA_WIDTH = axi.DATA_WIDTH
    slv.C_S_AXI_ADDR_WIDTH.set(ADDR_WIDTH)
    slv.C_S_AXI_DATA_WIDTH.set(DATA_WIDTH)
    ADDR_WIDTH.set(hInt(8))
    DATA_WIDTH.set(hInt(8))
 
    
if __name__ == "__main__":
    print(synthetizeCls(AxiLiteSlaveContainer, "axiLSlvCont"))
