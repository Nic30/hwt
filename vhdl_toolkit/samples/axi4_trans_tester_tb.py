import os

from vhdl_toolkit.axi_testbench import AXI4_slave, AXI_lite_master, AXI_testbench
from vhdl_toolkit.formater import formatVhdl 
from vhdl_toolkit.testbench_generator import entityFromFile
from vivado_toolkit.vivado_ip_wrap_fix import axi_m_integer_fix 


MODE_INIT = 0
MODE_R = 1
MODE_W = 2
MODE_RW = 3
MODE_DELAY_R = 4
MODE_DELAY_W = 5
MODE_FINALIZE = 6

DELAY_SAMPLES = 10


ADDR_STATUS_DATA          =0x10           
BITS_STATUS_DATA          =2              
ADDR_STATUS_CTRL          =0x14           
ADDR_MODE_V_DATA          =0x18           
BITS_MODE_V_DATA          =3              
ADDR_FRAME_CNT_DATA       =0x20           
BITS_FRAME_CNT_DATA       =32             
ADDR_FRAME_CNT_CTRL       =0x24           
ADDR_FRAME_SIZE_V_DATA    =0x28           
BITS_FRAME_SIZE_V_DATA    =9              
ADDR_BASE_ADDR_R_DATA     =0x30           
BITS_BASE_ADDR_R_DATA     =32             
ADDR_BASE_ADDR_W_DATA     =0x38           
BITS_BASE_ADDR_W_DATA     =32             
ADDR_DELAY_RESULTS_0_DATA =0x40           
BITS_DELAY_RESULTS_0_DATA =32             
ADDR_DELAY_RESULTS_0_CTRL =0x44           
ADDR_DELAY_RESULTS_1_DATA =0x48           
BITS_DELAY_RESULTS_1_DATA =32             
ADDR_DELAY_RESULTS_1_CTRL =0x4c           
ADDR_DELAY_RESULTS_2_DATA =0x50           
BITS_DELAY_RESULTS_2_DATA =32             
ADDR_DELAY_RESULTS_2_CTRL =0x54           
ADDR_DELAY_RESULTS_3_DATA =0x58           
BITS_DELAY_RESULTS_3_DATA =32             
ADDR_DELAY_RESULTS_3_CTRL =0x5c           
ADDR_DELAY_RESULTS_4_DATA =0x60           
BITS_DELAY_RESULTS_4_DATA =32             
ADDR_DELAY_RESULTS_4_CTRL =0x64           
ADDR_DELAY_RESULTS_5_DATA =0x68           
BITS_DELAY_RESULTS_5_DATA =32             
ADDR_DELAY_RESULTS_5_CTRL =0x6c           
ADDR_DELAY_RESULTS_6_DATA =0x70           
BITS_DELAY_RESULTS_6_DATA =32             
ADDR_DELAY_RESULTS_6_CTRL =0x74           
ADDR_DELAY_RESULTS_7_DATA =0x78           
BITS_DELAY_RESULTS_7_DATA =32             
ADDR_DELAY_RESULTS_7_CTRL =0x7c           
ADDR_DELAY_RESULTS_8_DATA =0x80           
BITS_DELAY_RESULTS_8_DATA =32             
ADDR_DELAY_RESULTS_8_CTRL =0x84           
ADDR_DELAY_RESULTS_9_DATA =0x88           
BITS_DELAY_RESULTS_9_DATA =32             
ADDR_DELAY_RESULTS_9_CTRL =0x8c           
ADDR_DELAY_RESULTS_10_DATA=0x90           
BITS_DELAY_RESULTS_10_DATA=32             
ADDR_DELAY_RESULTS_10_CTRL=0x94           
ADDR_DELAY_RESULTS_11_DATA=0x98           
BITS_DELAY_RESULTS_11_DATA=32             
ADDR_DELAY_RESULTS_11_CTRL=0x9c           
ADDR_DELAY_RESULTS_12_DATA=0xa0           
BITS_DELAY_RESULTS_12_DATA=32             
ADDR_DELAY_RESULTS_12_CTRL=0xa4           
ADDR_DELAY_RESULTS_13_DATA=0xa8           
BITS_DELAY_RESULTS_13_DATA=32             
ADDR_DELAY_RESULTS_13_CTRL=0xac           
ADDR_DELAY_RESULTS_14_DATA=0xb0           
BITS_DELAY_RESULTS_14_DATA=32             
ADDR_DELAY_RESULTS_14_CTRL=0xb4           
ADDR_DELAY_RESULTS_15_DATA=0xb8           
BITS_DELAY_RESULTS_15_DATA=32             
ADDR_DELAY_RESULTS_15_CTRL=0xbc           
ADDR_DELAY_RESULTS_16_DATA=0xc0           
BITS_DELAY_RESULTS_16_DATA=32             
ADDR_DELAY_RESULTS_16_CTRL=0xc4           
ADDR_DELAY_RESULTS_17_DATA=0xc8           
BITS_DELAY_RESULTS_17_DATA=32             
ADDR_DELAY_RESULTS_17_CTRL=0xcc           
ADDR_DELAY_RESULTS_18_DATA=0xd0           
BITS_DELAY_RESULTS_18_DATA=32             
ADDR_DELAY_RESULTS_18_CTRL=0xd4           
ADDR_DELAY_RESULTS_19_DATA=0xd8           
BITS_DELAY_RESULTS_19_DATA=32             
ADDR_DELAY_RESULTS_19_CTRL=0xdc           

ADDR_DELAY_RESULTS_DATA_BASE = ADDR_DELAY_RESULTS_0_DATA 
SPEP_DELAY_RESULTS_DATA = ADDR_DELAY_RESULTS_1_DATA - ADDR_DELAY_RESULTS_0_DATA

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
    def setMode(self, mode):
        self.axi4lite.write(ADDR_MODE_V_DATA, mode)
    def setup(self, baseAddr_r, baseAddr_w, frameSize, mode):
        self.setMode(MODE_INIT)
        self.axi4lite.write(ADDR_BASE_ADDR_R_DATA, baseAddr_r)
        self.axi4lite.write(ADDR_BASE_ADDR_W_DATA, baseAddr_w)
        self.axi4lite.write(ADDR_FRAME_SIZE_V_DATA, frameSize)
        # self.axi4lite.write(ADDR_AP_CTRL, 1);
        self.setMode(mode)
        # self.axi4lite.write(ADDR_AP_CTRL, 1 + 128);

    def readCNT(self):
        self.axi4lite.read(ADDR_FRAME_CNT_DATA)
    
    def readDelay(self):
        for i in range(DELAY_SAMPLES*2):
            self.axi4lite.read(ADDR_DELAY_RESULTS_DATA_BASE + i * SPEP_DELAY_RESULTS_DATA)
        

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

    axi4lite.read(ADDR_FRAME_CNT_DATA)
    for _ in range(10):
        axi4.readResp(0, [0xAAAA])
        # axi4.writeAccept([0xAAAA], withLast=i == 9)
    
    axi4lite.read(ADDR_FRAME_CNT_DATA)
    s = formatVhdl(tb.render())
    with open(outputFile, "w") as f:
        f.write(s)
    axi_m_integer_fix(os.path.join(projectSrcPath, "sources_1/bd/top/ip/top_axi4_trans_tester_0_0/sim/top_axi4_trans_tester_0_0.vhd"))
    print(s)

if __name__ == "__main__":
    axi4_tester() 
