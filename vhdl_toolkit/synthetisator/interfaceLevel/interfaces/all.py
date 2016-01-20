from vhdl_toolkit.synthetisator.interfaceLevel.interfaces.std import  BramPort, \
                 BramPort_withoutClk, Ap_hs, Ap_clk, Ap_rst_n, Ap_none
from vhdl_toolkit.synthetisator.interfaceLevel.interfaces.amba import Axi4, Axi4_xil,\
    AxiLite, AxiLite_xil, AxiStream 

allInterfaces = [Axi4, Axi4_xil,
 AxiLite,AxiLite_xil,
 BramPort, BramPort_withoutClk,
 AxiStream, Ap_hs, Ap_clk, Ap_rst_n, Ap_none
 ]