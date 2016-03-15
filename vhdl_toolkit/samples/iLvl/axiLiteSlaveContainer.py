from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_clk, \
    Ap_rst_n
from vhdl_toolkit.interfaces.amba import  AxiLite
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.param import Param

from vhdl_toolkit.samples.iLvl.axi_basic import AxiLiteBasicSlave

class AxiLiteSlaveContainer(Unit):
    ADDR_WIDTH = Param(8)
    DATA_WIDTH = Param(8)
    slv = AxiLiteBasicSlave()
    clk = Ap_clk(slv.S_AXI_ap_clk, isExtern=True)
    rst_n = Ap_rst_n(slv.S_AXI_ap_rst_n, isExtern=True)
    axi = AxiLite(slv.S_AXI, isExtern=True)
    slv.c_s_axi_addr_width.replace(ADDR_WIDTH)
    slv.c_s_axi_data_width.replace(DATA_WIDTH)

if __name__ == "__main__":

    u = AxiLiteSlaveContainer()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))
