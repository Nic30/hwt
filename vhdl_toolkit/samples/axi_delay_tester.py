import os
from vhdl_toolkit.axi_testbench import AXI4_slave, AXI_lite_master, AXI_testbench
from vhdl_toolkit.testbench_generator import entityFromFile
from vhdl_toolkit.formater import formatVhdl 
from vivado_toolkit.vivado_ip_wrap_fix import axi_m_integer_fix 

ADDR_AP_CTRL = 0x00
ADDR_GIE = 0x04
ADDR_IER = 0x08
ADDR_ISR = 0x0c
ADDR_BASEADDR_DATA = 0x10
BITS_BASEADDR_DATA = 32
ADDR_FRAMESIZE_DATA = 0x18
BITS_FRAMESIZE_DATA = 32
ADDR_RDWR_DATA = 0x20
BITS_RDWR_DATA = 1
ADDR_TIME_STORE_BASE = 0x40
ADDR_TIME_STORE_HIGH = 0x7f
WIDTH_TIME_STORE = 32
DEPTH_TIME_STORE = 11


def axi_delay_tester():
    projectSrcPath = "/home/nic30/Documents/vivado/axi_delay_tester_simple/axi_delay_tester_simple.srcs/"
    fileName = os.path.join(projectSrcPath, "sources_1/bd/top/hdl/top_wrapper.vhd")
    outputFile = os.path.join(projectSrcPath, "sim_1/new/axi_delay_tester_simple_tb.vhd")
    entity = entityFromFile(fileName)

    tb = AXI_testbench(entity)
    axi4lite = AXI_lite_master('s_axi_AXILiteS_r_')
    axi4 = AXI4_slave('m_axi_axi_')
    tb.register(axi4lite)
    tb.register(axi4)
    tb.delay(10)
    
    axi4lite.write(ADDR_RDWR_DATA, 0)
    axi4lite.write(ADDR_FRAMESIZE_DATA, 1)
    axi4lite.write(ADDR_BASEADDR_DATA, 0)
    axi4lite.write(ADDR_AP_CTRL, 1)
    
    for _ in range(10):
        axi4.readResp([0])
    
    for i in range(11):
        axi4lite.read(ADDR_TIME_STORE_BASE + i * 4)
        
    s = formatVhdl(tb.render())
    # with open(outputFile, "w") as f:
    #    f.write(s)
    # axi_m_integer_fix(os.path.join(projectSrcPath, "sources_1/bd/top/ip/top_axi4_trans_tester_coordinator_0_0/sim/top_axi4_trans_tester_coordinator_0_0.vhd"))
    print(s)


if __name__ == "__main__":
    axi_delay_tester()
