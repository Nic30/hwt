from vhdl_toolkit.synthetisator.context import Context
from vhdl_toolkit.parser import entityFromFile
from vhdl_toolkit.synthetisator.unit import VHDLUnit, automapSigs
from vivado_toolkit.ip_packager.busInterface import AXILite, Axi_channeled, \
    Ap_rst_n, Ap_clk, HsAXIStream, HS_config_d_V
from vhdl_toolkit.synthetisator.signal import signalsForInterface
from vhdl_toolkit.synthetisator.example import connectUnits
from vhdl_toolkit.formater import formatVhdl


def superDMA_complex():
    c = Context("superDMA_complex")
    interf = []          
    # nterf, c = dualportRam(512, 64)   

    ch_cnt = 2
    dma = VHDLUnit(entityFromFile("/home/nic30/Documents/vivado/toolkitTest/toolkitTest.srcs/sources_1/new/superDMA/src/superDMA.vhd"))
    axi_regs = VHDLUnit(entityFromFile("/home/nic30/Documents/vivado/toolkitTest/toolkitTest.srcs/sources_1/new/axi_regs_with_def_value/src/axi_regs_with_def_value.vhd"))
    e_inBuff = entityFromFile("/home/nic30/Documents/vivado/toolkitTest/toolkitTest.srcs/sources_1/new/InputBuffer/src/InputBuffer.vhd")
    e_blockRam = entityFromFile("/home/nic30/Documents/vivado/toolkitTest/toolkitTest.srcs/sources_1/new/dualportRAM.vhd")

    axiLite_interf = AXILite(32, 32)
    ACP_interf = Axi_channeled(3, 32, 64)
    HP_interf = Axi_channeled(3, 32, 64) 

    axiLite = signalsForInterface(c, axiLite_interf, "s_axi_AXILiteS")
    rst = signalsForInterface(c, Ap_rst_n())
    clk = signalsForInterface(c, Ap_clk())
    MBus0 = signalsForInterface(c, ACP_interf, "m_mbus_0")
    MBus1 = signalsForInterface(c, HP_interf, "m_mbus_1")
    
    automapSigs(axi_regs, clk)
    automapSigs(axi_regs, rst)
    
    dma.genericsValues['C_S_AXI_AXILITES_ADDR_WIDTH'] = axiLite_interf.A_WIDTH
    dma.genericsValues['C_S_AXI_AXILITES_DATA_WIDTH'] = axiLite_interf.D_WIDTH
    automapSigs(dma, MBus0, lambda x: x.replace("m_mbus_0", "len_bus"))
    automapSigs(dma, MBus1, lambda x: x.replace("m_mbus_1", "data_bus"))
    
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
        
        OTHERS_WIDTH = 16
        for sigName in  ["space2read", "space2write"]:
            toDMA = c.sig(sigName + 'ToDMA_' + str(i), OTHERS_WIDTH)
            connectUnits(toDMA, dma, axi_regs, sigName + "_" + str(i) + "_i"  , sigName + "_out_" + str(i))
            fromDMA = c.sig(sigName + "FromDMA_" + str(i) , OTHERS_WIDTH)
            connectUnits(fromDMA, axi_regs, dma, sigName + "_in_" + str(i), sigName + "_" + str(i) + "_o")

    
    rst[0].connectToPortByName(dma, 'ap_start')
    rst[0].connectToPortByName(dma, 'ap_continue')
        
    dmaSigs = []
    for i in [clk, rst, axiLite]:
        dmaSigs.extend(i)
    automapSigs(dma, dmaSigs)
    interf.extend(dmaSigs)
    interf.extend(MBus0)
    interf.extend(MBus1)

    return [interf, c]


if __name__ == "__main__":
    interf, c = superDMA_complex()
    with open("/home/nic30/Documents/vivado/toolkitTest/toolkitTest.srcs/sources_1/new/top_test.vhd", "w") as f:
        for o in c.synthetize("test_top", interf):
            f.write(formatVhdl(str(o)))
    print("done")
