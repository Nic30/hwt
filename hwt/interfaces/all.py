from hwt.interfaces.std import  BramPort, \
                 BramPort_withoutClk, Handshaked, Clk, Rst_n, Signal, Rst, RdSynced, VldSynced
#from hwtLib.amba.amba import Axi4, Axi4_xil, \
#    AxiLite, AxiLite_xil, AxiStream, AxiStream_withoutSTRB, AxiStream_withUserAndStrb, \
#    AxiStream_withUserAndNoStrb 

allInterfaces = [#Axi4, Axi4_xil,
   #AxiLite, AxiLite_xil,
   BramPort, BramPort_withoutClk,
   #AxiStream_withUserAndStrb, AxiStream, AxiStream_withUserAndNoStrb, AxiStream_withoutSTRB,
   Handshaked,  Clk, Rst, Rst_n, VldSynced, RdSynced, Signal
 ]
