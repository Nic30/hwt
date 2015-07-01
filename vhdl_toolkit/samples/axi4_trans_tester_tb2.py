import os
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.axi_testbench import AXI_testbench, AXI_lite_master, \
    AXI4_slave
from vhdl_toolkit.samples.axi4_trans_tester_tb import axi_tester, ADDR_CNT_DATA, \
    MODE_R, MODE_W, MODE_DELAY_R

from vhdl_toolkit.formater import formatVhdl
from vivado_toolkit.vivado_ip_wrap_fix import axi_m_integer_fix
from vhdl_toolkit.testbench_generator import delay
from python_toolkit.arrayQuery import single



def axi4_tester():
    projectSrcPath = "/home/nic30/Documents/vivado/axi_trans_tester2/axi_trans_tester2.srcs"
    fileName = os.path.join(projectSrcPath, "sources_1/bd/top_axi_trans_tester_complex/hdl/top_axi_trans_tester_complex_wrapper.vhd")
    outputFile = os.path.join(projectSrcPath, "sim_1/new/top_axi_trans_tester_complex_tb.vhd")
    entity = entityFromFile(fileName)
    
    IDs_CNT = 2
    frameSize = 4
    # listAxiIterfaces(entity)
    tb = AXI_testbench(entity)
  
    axi4lite = AXI_lite_master('s_axi_AXILiteS_r_')
    axi4 = AXI4_slave('m_axi_')
    tb.register(axi4lite)
    tb.register(axi4)
    tester = axi_tester(axi4lite)
    def axiDelay(ch, clk):
        single(tb.processes, lambda p : p.name == axi4.prefix + ch).bodyBuff += [delay(clk)]
        
    def axiLiteDelay(clk):
        single(tb.processes, lambda p : p.name == axi4lite.prefix + "proc").bodyBuff += [delay(clk)]
    def rd_test():
        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_R)
    
        axi4lite.read(ADDR_CNT_DATA)
        
        for i in range(10):
            axi4.readResp(128, [i for i in range(frameSize)], burstId=i % IDs_CNT)
            axiDelay("R", 3)
            axiDelay("AR", 4 + frameSize)
            # axi4.writeAccept(expectedAddr, data, withLast)
        axiLiteDelay(10)
        tester.readCNT()
        # axiLiteDelay(10)
        # tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_R)
        # for i in range(30):
        #    axi4.readResp(128, [i for i in range(frameSize)], burstId=i % IDs_CNT)
        # axiLiteDelay(30 * frameSize)
    def wr_test():
        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_W)
        for i in range(10):
            axi4.writeAccept(0, [0 for _ in range(frameSize)])
        axiLiteDelay(frameSize * 10)
        tester.readCNT()
    def delay_test():
        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=1, mode=MODE_DELAY_R)
        for i in range(10):
            axi4.readResp(128, [1], burstId=i % 2)
            axiDelay("AR", 3)
        axiLiteDelay(50)
        tester.readCNT()

    def mixed():
        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_R)
        for i in range(10):
            axi4.readResp(128, [i for i in range(frameSize)], burstId=i % IDs_CNT)
            axi4.writeAccept(0, [1 for _ in range(frameSize)])
    # wr_test()
    rd_test()
    # delay_test()
    # mixed()
    
    tester.readCNT()
    s = formatVhdl(tb.render())
    with open(outputFile, "w") as f:
        f.write(s)
    # axi_m_integer_fix(os.path.join(projectSrcPath, "sources_1/bd/top/ip/top_axi4_trans_tester_0_0/sim/top_axi4_trans_tester_0_0.vhd"))
    print(s)

if __name__ == "__main__":
    axi4_tester() 
