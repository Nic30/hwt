from vhdl_toolkit.synthetisator.context import Context
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.unit import VHDLUnit, automapSigs
from vivado_toolkit.ip_packager.busInterface import AXILite, Axi_channeled, \
    Ap_rst_n, Ap_clk, HsAXIStream, HS_config_d_V, BlockRamPort
from vhdl_toolkit.synthetisator.signal import signalsForInterface
from vhdl_toolkit.synthetisator.example import connectUnits
from vhdl_toolkit.formater import formatVhdl
from python_toolkit.arrayQuery import single


def superDMA_complex():
    c = Context("superDMA_complex")
    interf = []          
    # nterf, c = dualportRam(512, 64)   

    ch_cnt = 2
    workspace = "/home/nic30/Documents/vivado/toolkitTest/toolkitTest.srcs/sources_1/new/"
    dma = VHDLUnit(entityFromFile(workspace + "superDMA/src/superDMA.vhd"))
    axi_regs = VHDLUnit(entityFromFile(workspace + "axi_regs_with_def_value/src/axi_regs_with_def_value.vhd"))
    axiSplit = VHDLUnit(entityFromFile(workspace + 'axi_lite_split/axi_lite_split.vhd'))
    e_inBuff = entityFromFile(workspace + "InputBuffer/src/InputBuffer.vhd")
    e_blockRam = entityFromFile(workspace + "dualportRAM.vhd")
    

    axiLite_interf = AXILite(32, 32)
    ACP_interf = Axi_channeled(3, 32, 64)
    HP_interf = Axi_channeled(3, 32, 64) 

    rst = signalsForInterface(c, Ap_rst_n())
    clk = signalsForInterface(c, Ap_clk())
    axiLite = signalsForInterface(c, axiLite_interf, "S_AXI")
    axiLite2DMA = signalsForInterface(c, axiLite_interf, "AXI_TO_DMA")
    axiLite2REGS = signalsForInterface(c, axiLite_interf, "AXI_TO_REGS")
    MBus0 = signalsForInterface(c, ACP_interf, "m_mbus_0")
    MBus1 = signalsForInterface(c, HP_interf, "m_mbus_1")
    
    
    
    # connect axiSplit
    def regularAxi2axiOnAxi_regs(name):
        name = name.lower()
        for n in ["addr", "data", "resp", "strb" ]:
            if name.endswith(n):
                name = name + "_V"
        for orig, new in [("axi_to_regs", "axilite"), \
                          ("_r", "_r_"), ("_ar", "_ar_"), \
                          ("_aw", "_aw_"), ("_w", "_w_"), \
                          ("_b", "_b_") ]:
            name = name.replace(orig, new)
        return name
    
    axiSplit.genericsValues["C_AXI_ADDR_WIDTH"] = axiLite_interf.A_WIDTH
    axiSplit.genericsValues["C_AXI_DATA_WIDTH"] = axiLite_interf.D_WIDTH
    axiSplit.genericsValues["C_INPUT_REG"] = False
    axiSplit.genericsValues["C_SPLIT_ADDRESS"] = 4096
    
    
    automapSigs(axiSplit, axiLite)
    automapSigs(axiSplit, clk, lambda x: x.replace("ap_clk", "ACLK"))
    automapSigs(axiSplit, rst, lambda x: x.replace("ap_rst_n", "ARESETN"))
    
    automapSigs(axiSplit, axiLite2DMA, lambda x: x.replace("AXI_TO_DMA", "M0_AXI"))
    automapSigs(dma, axiLite2DMA, lambda x: x.replace("AXI_TO_DMA", "s_axi_AXILiteS"))
    
    automapSigs(axiSplit, axiLite2REGS, lambda x: x.replace("AXI_TO_REGS", "M1_AXI"))
    automapSigs(axi_regs, axiLite2REGS, regularAxi2axiOnAxi_regs)
        
    # connect axiRegs    
    automapSigs(axi_regs, clk)
    automapSigs(axi_regs, rst)
    
    # connect DMA
    dma.genericsValues['C_S_AXI_AXILITES_ADDR_WIDTH'] = axiLite_interf.A_WIDTH
    dma.genericsValues['C_S_AXI_AXILITES_DATA_WIDTH'] = axiLite_interf.D_WIDTH
    automapSigs(dma, MBus0, lambda x: x.replace("m_mbus_0", "len_bus"))
    automapSigs(dma, MBus1, lambda x: x.replace("m_mbus_1", "data_bus"))
    
    # connect BRAM
    for descrType in ["r", "w"]:
        blockRAM = VHDLUnit(e_blockRam)
        blockRAM.genericsValues["C_DATA_WIDTH"] = HP_interf.D_WIDTH
        blockRAM.genericsValues["C_ADDR_WIDTH"] = 9
        
        for rw, port in [("rd", "a"), ("wr", "b")]:
            connectionPrefix = "descrBM_" + descrType + "_" + rw
            def bmInterfName2bmInterf(name):
                name = name.replace(connectionPrefix, port)
                name = name.lower()
                if name.endswith("_v"):
                        name = name[:-2]
                
                return name 
            connections = signalsForInterface(c, BlockRamPort(9, 64), connectionPrefix)
            bramclk = single(connections, lambda x: x.name.endswith("clk"))
            bramclk.assign(clk[0])
            # connect DMA and blockRam
            automapSigs(blockRAM, connections, bmInterfName2bmInterf)
            automapSigs(dma, connections)

    
    for i in range(ch_cnt):
        buff = VHDLUnit(e_inBuff)
        # connect inputBuffers
        data_in = signalsForInterface(c, HsAXIStream(64), "data_in_" + str(i))
        data_in_len = signalsForInterface(c, HS_config_d_V(13), "data_in_len_" + str(i))
        data_in2dma = signalsForInterface(c, HsAXIStream(64), "data_in2dma_" + str(i))
        
        automapSigs(buff, rst)
        automapSigs(buff, clk)
        # data_in in buffer
        automapSigs(buff, data_in, lambda x : x.replace("data_in_" + str(i), "data_in"))
        interf.extend(data_in)
        # data_in_len
        automapSigs(buff, data_in_len, lambda x : x.replace("data_in_len_" + str(i), "lengths"))
        automapSigs(dma, data_in_len)
        # data_in2dma
        automapSigs(buff, data_in2dma, lambda x : x.replace("data_in2dma_" + str(i), "data_out"))
        automapSigs(dma, data_in2dma, lambda x: x.replace("data_in2dma_" + str(i), "data_in_" + str(i)))
        
        # data_out from dma
        data_out = signalsForInterface(c, HsAXIStream(64), "data_out_" + str(i))
        automapSigs(dma, data_out)
        
        # connect external axi registers
        OTHERS_WIDTH = 16
        for sigName in  ["space2read", "space2write"]:
            toDMA = c.sig(sigName + 'ToDMA_' + str(i), OTHERS_WIDTH)
            connectUnits(toDMA, dma, axi_regs, sigName + "_" + str(i) + "_i"  , sigName + "_out_" + str(i))
            fromDMA = c.sig(sigName + "FromDMA_" + str(i) , OTHERS_WIDTH)
            connectUnits(fromDMA, axi_regs, dma, sigName + "_in_" + str(i), sigName + "_" + str(i) + "_o")
    
    rst[0].connectToPortByName(dma, 'ap_start')
    rst[0].connectToPortByName(dma, 'ap_continue')
        
    dmaSigs = []
    for i in [clk, rst]:
        dmaSigs.extend(i)
    automapSigs(dma, dmaSigs)
    for i in [dmaSigs, axiLite, MBus0, MBus1]:
        interf.extend(i)

    return [interf, c]


if __name__ == "__main__":
    interf, c = superDMA_complex()
    with open("/home/nic30/Documents/vivado/toolkitTest/toolkitTest.srcs/sources_1/new/superDMA_complex.vhd", "w") as f:
        for o in c.synthetize("superDMA_complex", interf):
            f.write(formatVhdl(str(o)))
    print("done")
