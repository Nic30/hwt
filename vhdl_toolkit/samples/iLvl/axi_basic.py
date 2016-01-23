from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit, UnitWithSource
from vhdl_toolkit.synthetisator.interfaceLevel.interfaces.std import Ap_clk, \
    Ap_rst_n
from vhdl_toolkit.synthetisator.interfaceLevel.interfaces.amba import  AxiLite
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.param import Param


class AxiLiteBasicSlave(UnitWithSource):
    _origin = "vhdl/axiLite_basic_slave.vhd"
    
    
class AxiLiteSlaveContainer(Unit):
    ADDR_WIDTH = Param(8)
    DATA_WIDTH = Param(8)
    slv = AxiLiteBasicSlave()
    clk = Ap_clk(slv.S_AXI_ACLK, isExtern=True)
    rst_n = Ap_rst_n(slv.S_AXI_ARESETN, isExtern=True)
    axi = AxiLite(slv.S_AXI, isExtern=True)
    slv.C_S_AXI_ADDR_WIDTH.inherit(ADDR_WIDTH)
    slv.C_S_AXI_DATA_WIDTH.inherit(DATA_WIDTH)



if __name__ == "__main__":

    u = AxiLiteSlaveContainer()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))
    # sys.setrecursionlimit(3000)
    # pr = cProfile.Profile()
    # pr.enable()
    # u = AxiLiteBasicSlave()
    # # u = AxiLiteSlaveContainer()
    #
    # pr.disable()
    # s = io.StringIO()
    # sortby = 'time'
    # ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    # ps.print_stats(10)
    # print(s.getvalue())
    #
    #
    # s = [ formatVhdl(str(x)) for x in u._synthesise()]
    # # print("\n".join(s))
