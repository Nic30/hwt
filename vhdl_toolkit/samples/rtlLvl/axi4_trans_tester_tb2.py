import os

from python_toolkit.arrayQuery import single
from vhdl_toolkit.samples.rtlLvl.axi_testbench import AXI_testbench, AXI_lite_master, \
    AXI4_slave
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.samples.rtlLvl.axi4_trans_tester_tb import axi_tester, \
    MODE_R, MODE_W, MODE_DELAY_R, MODE_DELAY_W, MODE_INIT
from vhdl_toolkit.testbench_generator import delay


def axi4_tester():
    projectSrcPath = "/home/nic30/Documents/vivado/axi_trans_tester2/axi_trans_tester2.srcs"
    fileName = os.path.join(projectSrcPath, "sources_1/bd/axi_tester_complex/hdl/axi_tester_complex_wrapper.vhd")
    outputFile = os.path.join(projectSrcPath, "sim_1/new/axi_tester_complex_wrapper_tb.vhd")
    entity = entityFromFile(fileName)
    
    IDs_CNT = 2
    frameSize = 30
    # listAxiIterfaces(entity)
    tb = AXI_testbench(entity)
  
    axi4lite = AXI_lite_master('s_axi_AXILiteS_r_')
    axi4 = AXI4_slave('m_axi_')
    tb.register(axi4lite)
    tb.register(axi4)
    tester = axi_tester(axi4lite)

    def axiDelay(ch, clk):
        p= single(tb.processes, lambda p : p.name == axi4.prefix + ch)
        p.bodyBuff += [delay(clk)]

    def axiLiteDelay(clk):
        single(tb.processes, lambda p : p.name == axi4lite.prefix + "proc").bodyBuff += [delay(clk)]

    def rd_test():
        tester.setup(baseAddr_r=256, baseAddr_w=128, frameSize=frameSize, mode=MODE_R)
        tester.readCNT()
        
        for i in range(10):
            axi4.readResp(256, [i for i in range(frameSize)], burstId=i % IDs_CNT)
            # axiDelay("R", 3)
            # axiDelay("AR", 4 + frameSize)
            # axi4.writeAccept(expectedAddr, data, withLast)
            tester.readCNT()
        # axiLiteDelay(10)
        
        # axiLiteDelay(10)
        # tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_R)
        # for i in range(30):
        #    axi4.readResp(128, [i for i in range(frameSize)], burstId=i % IDs_CNT)
        # axiLiteDelay(30 * frameSize)
    def wr_test():
        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_W)
        for i in range(10):
            axi4.writeAccept(0, [0 for _ in range(frameSize)])
            tester.readCNT()
        axiLiteDelay(frameSize * 10)
        tester.readCNT()
        
    def delayR_test():
        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_DELAY_R)
        for i in range(10):
            axi4.readResp(128, range(frameSize), burstId=i % IDs_CNT)
            axiDelay("AR", 4)
            axiDelay("R", 5)
        axiLiteDelay(300)
        tester.readDelay()
        tester.setMode(MODE_INIT)
        axiLiteDelay(50)

        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_DELAY_R)
        for i in range(10):
            axi4.readResp(128, range(frameSize), burstId=i % IDs_CNT)
            axiDelay("AR", 4)
            axiDelay("R", 5)
        axiLiteDelay(300)
        tester.readDelay()
        
        
    def delayW_test():
        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_DELAY_W)
        for i in range(10):
            axi4.writeAccept(128, range(frameSize))
            #axiDelay("AW", 4)
            axiDelay("W", 5)
        axiLiteDelay(250)
        tester.readDelay()

    def mixed():
        tester.setup(baseAddr_r=0, baseAddr_w=128, frameSize=frameSize, mode=MODE_R)
        for i in range(12):
            axi4.readResp(128, [i for i in range(frameSize)], burstId=i % IDs_CNT)
            axi4.writeAccept(0, [1 for _ in range(frameSize)])
    #wr_test()
    # rd_test()
    delayR_test()
    #delayW_test()
    # mixed()
    
    tester.readCNT()
    s = formatVhdl(tb.render())
    with open(outputFile, "w") as f:
        f.write(s)
    # axi_m_integer_fix(os.path.join(projectSrcPath, "sources_1/bd/top/ip/top_axi4_trans_tester_0_0/sim/top_axi4_trans_tester_0_0.vhd"))
    #print(s)

if __name__ == "__main__":
    axi4_tester() 
