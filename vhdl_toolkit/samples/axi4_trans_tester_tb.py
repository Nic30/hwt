import os
from vhdl_toolkit.axi_testbench import AXI4_slave, AXI_lite_master, AXI_testbench
from vhdl_toolkit.testbench_generator import entityFromFile
from vhdl_toolkit.formater import formatVhdl 
from vivado_toolkit.vivado_ip_wrap_fix import axi_m_integer_fix 

MODE_INIT =0
MODE_R    =1
MODE_W    =2
MODE_RW   =3
MODE_DELAY_R =4

ADDR_AP_CTRL               =0x00
ADDR_GIE                   =0x04
ADDR_IER                   =0x08
ADDR_ISR                   =0x0c
ADDR_CNT_DATA              =0x10
BITS_CNT_DATA              =32
ADDR_CNT_CTRL              =0x14
ADDR_MODE_DATA           =0x18
BITS_MODE_DATA           =3
ADDR_FRAME_SIZE_DATA     =0x20
BITS_FRAME_SIZE_DATA     =12
ADDR_BASE_ADDR_R_DATA      =0x28
BITS_BASE_ADDR_R_DATA      =32
ADDR_BASE_ADDR_W_DATA      =0x30
BITS_BASE_ADDR_W_DATA      =32
ADDR_DELAY_RESULTS_0_I_DATA=0x38
BITS_DELAY_RESULTS_0_I_DATA=32
ADDR_DELAY_RESULTS_0_O_DATA=0x40
BITS_DELAY_RESULTS_0_O_DATA=32
ADDR_DELAY_RESULTS_0_O_CTRL=0x44   

# def coordinator():
#    projectSrcPath = "/home/nic30/Documents/vivado/axi4_tester_coordinator_simple/axi4_tester_coordinator_simple.srcs/"
#    fileName = os.path.join(projectSrcPath, "sources_1/bd/top/hdl/top_wrapper.vhd")
#    outputFile = os.path.join(projectSrcPath, "sim_1/new/axi4_tester_coordinator_tb.vhd")
#    entity = entityFromFile(fileName)
#    # listAxiIterfaces(entity)
#    tb = AXI_testbench(entity)
#    axi4lite = AXI_lite_master('s_axi_AXILiteS_r_')
#    axi4 = AXI4_slave('m_axi_gmem64_')
#    tb.register(axi4lite)
#    tb.register(axi4)
#    tb.delay(10)
#    
#    axi4lite.write(TESTER_ADDR_REG, 0x01)
#    axi4lite.write(DELAY_REG, 30)
#    axi4lite.write(ADDR_AP_CTRL, 1)
#    
#    axi4.writeAccept(range(4))
#        
#    s = formatVhdl(tb.render())
#    with open(outputFile, "w") as f:
#        f.write(s)
#    axi_m_integer_fix(os.path.join(projectSrcPath, "sources_1/bd/top/ip/top_axi4_trans_tester_coordinator_0_0/sim/top_axi4_trans_tester_coordinator_0_0.vhd"))
#    print(s)


class axi_tester():
    def __init__(self, axi4lite):
        self.axi4lite = axi4lite  
    def setup(self, baseAddr_r, baseAddr_w, frameSize, mode):
        self.axi4lite.write(ADDR_MODE_DATA, MODE_INIT)
        self.axi4lite.write(ADDR_BASE_ADDR_R_DATA, baseAddr_r)
        self.axi4lite.write(ADDR_BASE_ADDR_W_DATA, baseAddr_w)
        self.axi4lite.write(ADDR_FRAME_SIZE_DATA, frameSize)
        self.axi4lite.write(ADDR_AP_CTRL, 1);
        self.axi4lite.write(ADDR_MODE_DATA, mode)
        self.axi4lite.write(ADDR_AP_CTRL, 1 + 128);

    def readCNT(self):
        self.axi4lite.read(ADDR_CNT_DATA)
    
    def readDelay(self):
        self.axi4lite.read(ADDR_DELAY_RESULTS_0_O_DATA)
        

def axi4_tester():
    projectSrcPath = "/home/nic30/Documents/vivado/axi4_tester_simple/axi4_tester_simple.srcs"
    fileName = os.path.join(projectSrcPath, "sources_1/bd/top/hdl/top_wrapper.vhd")
    outputFile = os.path.join(projectSrcPath, "sim_1/new/top_wraper_tb.vhd")
    entity = entityFromFile(fileName)
    # listAxiIterfaces(entity)
    tb = AXI_testbench(entity)
    axi4lite = AXI_lite_master('s_axi_AXILiteS_r_')
    axi4 = AXI4_slave('m_axi_data_')
    tb.register(axi4lite)
    tb.register(axi4)
    tester = axi_tester(axi4lite)
    tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=1, mode=MODE_R)

    axi4lite.read(ADDR_CNT_DATA)
    for _ in range(10):
        axi4.readResp(0, [0xAAAA])
        # axi4.writeAccept([0xAAAA], withLast=i == 9)
    
    axi4lite.read(ADDR_CNT_DATA)
    s = formatVhdl(tb.render())
    with open(outputFile, "w") as f:
        f.write(s)
    axi_m_integer_fix(os.path.join(projectSrcPath, "sources_1/bd/top/ip/top_axi4_trans_tester_0_0/sim/top_axi4_trans_tester_0_0.vhd"))
    print(s)

if __name__ == "__main__":
    axi4_tester() 
