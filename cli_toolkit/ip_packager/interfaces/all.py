from hdl_toolkit.interfaces.std import BramPort, Clk, Rst, Rst_n
from hdl_toolkit.interfaces.amba import AxiLite, AxiLite_xil, AxiStream, \
    AxiStream_withoutSTRB, AxiStream_withUserAndNoStrb, \
    AxiStream_withUserAndStrb, Axi4
from hdl_toolkit.interfaces.peripheral import I2c, Uart
from cli_toolkit.ip_packager.interfaces.std import IP_BlockRamPort, IP_Clk, \
    IP_Rst, IP_Rst_n
from cli_toolkit.ip_packager.interfaces.amba import IP_AXILite, IP_AXIStream, \
    IP_Axi4
from cli_toolkit.ip_packager.interfaces.peripheral import IP_IIC, IP_Uart


allBusInterfaces = { BramPort : IP_BlockRamPort,
                     AxiLite : IP_AXILite,
                     AxiLite_xil : IP_AXILite,
                     AxiStream : IP_AXIStream,
                     
                     AxiStream_withoutSTRB :  IP_AXIStream,
                     AxiStream_withUserAndNoStrb : IP_AXIStream,
                     AxiStream_withUserAndStrb : IP_AXIStream,
                     
                     Axi4 : IP_Axi4,
                     Clk : IP_Clk,
                     Rst : IP_Rst,
                     Rst_n : IP_Rst_n,
                     I2c : IP_IIC,
                     Uart: IP_Uart
                    }
