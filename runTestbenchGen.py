from python_toolkit.arrayQuery import single
from vhdl_toolkit.axi_testbench import AXI_lite_master
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.process import HWProcess
from vhdl_toolkit.testbench_generator import TestbenchCreator, AxiStream, delay, \
    hs, vecAsig, vhdlErr, asUnsigned


class SuperDMA():
    def __init__(self, axiLite, axiLite2, ch_cnt):
        self.axiLite = axiLite
        self.axiLite2 = axiLite2
        self.ch_cnt = ch_cnt
        self.INFO_ADDR = 0x10
        self.LENBUFF_ADDR = 0x1c

        if ch_cnt == 4:
            self.BASEDESCRW = 0x44
            self.BASEDESCR_INIT = 0x64
            self.SPACE2READ = 0x6c
            self.SPACE2WRITE = 0x8c
            self.READERPOSS = 0xac
        elif ch_cnt == 2:
            self.BASEDESCRR = 0x24
            self.BASEDESCRW = 0x34
            self.BASEDESCR_INIT = 0x44
            self.SPACE2READ = 0x0
            self.SPACE2WRITE = ch_cnt * 4
            self.BASEDESCR_STEP = 8
            self.SPACE2_STEP = 4
            self.READERPOSS = 0x8c
        
    def hwInit(self, space2read, space2write):
        a = self.axiLite
        a2 = self.axiLite2
        buff = []
        buff += [ a2.write(self.LENBUFF_ADDR, 1), delay(1)  ]
        for i in range(self.ch_cnt):
            buff += [ a2.write(self.BASEDESCRR + i * self.BASEDESCR_STEP, 4096 * (i + 1)), delay(2) ]
            buff += [ a2.write(self.BASEDESCRW + i * self.BASEDESCR_STEP, 4096 * (i + self.ch_cnt + 1)), delay(2) ]
        buff += [ a2.write(self.BASEDESCR_INIT, 1), a2.write(self.BASEDESCR_INIT, 0), delay(1)]
        buff += [ a.write(self.SPACE2READ + i * self.SPACE2_STEP, space2read) for i in range(self.ch_cnt) ]
        buff += [ a.write(self.SPACE2WRITE + i * self.SPACE2_STEP, space2write) for i in range(self.ch_cnt)]

        buff += [ delay(5), a2.read(self.INFO_ADDR)]
        
        return buff 

        
def InputBuffer_tb():
    fileName = "/home/nic30/Documents/vivado/superdma_inBuff_basic/superdma_inBuff_basic.srcs/sources_1/bd/top/hdl/top_wrapper.vhd"
    tb_fileName = "/home/nic30/Documents/vivado/superdma_inBuff_basic/superdma_inBuff_basic.srcs/sim_1/new/top_tb.vhd"
    entity = entityFromFile(fileName)
    tb = TestbenchCreator(entity)
    tb.addClkProcess()
    stimP = tb.addStimProcess(initialResetDelay=2)
    data_in = AxiStream("data_in")
    data_out = AxiStream("data_out")
    lengths = hs("lengths_v_v")
    lengths.data = "_data"
    
    # for l in range(5):
    #    for i in range(l):
    #        stimP.bodyBuff += [data_in.write(i, i==l-1)]
    #        stimP.bodyBuff += [delay(1)]
    #    stimP.bodyBuff += [data_in.write_stop()]
    burstLen = 4096 // 8
    for i in range(burstLen):
        stimP.bodyBuff += [data_in.write(i, i == (burstLen - 1))]
        stimP.bodyBuff += [delay(1)]
    stimP.bodyBuff += [data_in.write_stop()]


    for l in range(5):
        stimP.bodyBuff += [data_out.read()]
        stimP.bodyBuff += [lengths.read()]
        stimP.bodyBuff += [delay(1)]
        
    stimP.bodyBuff += [lengths.read_stop()]

    
    
    tb_str = formatVhdl(tb.render())     
    with open(tb_fileName , "w") as f:
        f.write(tb_str)
    print(tb_str)

def DDM_tb():
    fileName = "/home/nic30/Documents/vivado/ddm_test/ddm_test.srcs/sources_1/bd/ddm_test/hdl/ddm_test_wrapper.vhd"
    tb_fileName = "/home/nic30/Documents/vivado/ddm_test/ddm_test.srcs/sim_1/new/ddm_test_tb.vhd"
    
    CH_CNT = 2
    
    entity = entityFromFile(fileName)
    tb = TestbenchCreator(entity)
    tb.addClkProcess()

    stimP = tb.addStimProcess(initialResetDelay=2)
    stimP.bodyBuff += [ "ap_start <= '1';", "ap_continue <= '1';" ]
    stimP.bodyBuff += [ vecAsig("descrRem_%d_V" % (ch), 511) for ch in range(CH_CNT)]
    stimP.bodyBuff += [ vecAsig("space_%d_i" % (ch), 256) for ch in range(CH_CNT)]
    stimP.bodyBuff += [ vhdlErr((asUnsigned("req_%d_LEN_V") + " = 255") % i, "req_%d_LEN_v is good" % i) for i in  range(CH_CNT)]
    stimP.bodyBuff += [ vhdlErr((asUnsigned("req_%d_ADDR_V") + " = 0") % i, "req_%d_ADDR_V is good" % i) for i in  range(CH_CNT)]

    tb_str = formatVhdl(tb.render())     
    with open(tb_fileName , "w") as f:
        f.write(tb_str)
    print(tb_str)

def SuperDMA_tb():
    fileName = "/home/nic30/Documents/vivado/superdma_basic/superdma_basic.srcs/sources_1/bd/top/hdl/top_wrapper.vhd"
    tb_fileName = "/home/nic30/Documents/vivado/superdma_basic/superdma_basic.srcs/sim_1/new/top_tb.vhd"
    entity = entityFromFile(fileName)
    tb = TestbenchCreator(entity)
    tb.addClkProcess()
    stimP = tb.addStimProcess(initialResetDelay=2)
    axiLite = AXI_lite_master("axilite_")
    axiLite2 = AXI_lite_master("s_axi_axilites_")
    dma = SuperDMA(axiLite, axiLite2, 2)
    stimP.bodyBuff += dma.hwInit(600, 600)
    def registerMultiple(iterableInterfaces):
        for i in iterableInterfaces:
            proc = HWProcess(i.name + "proc")
            proc.register(i)
            tb.processes.append(proc)
            
    
    dataIn = [ AxiStream("data_in_" + str(indx), "clk_period") for indx in range(dma.ch_cnt) ]
    dataOut = [ AxiStream("data_out_" + str(indx), "clk_period") for indx in range(dma.ch_cnt)]
 
        
    registerMultiple(dataIn + dataOut)
    for i in dataOut:
        i.readBurst(range(511))
        i.readBurst(range(511))
    for i in dataIn:
        i.writeBurst(range(511))
        # single(tb.processes, lambda x : x.name == i.name+"proc").bodyBuff.append(delay(4096*2))
        i.writeBurst(range(511))

    
    tb_str = formatVhdl(tb.render())     
    with open(tb_fileName , "w") as f:
        f.write(tb_str)
        
        
        
    print(tb_str)
    

if __name__ == "__main__":
    SuperDMA_tb()
    # DDM_tb()
