from hdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from hdl_toolkit.interfaces.std import FifoReader, FifoWriter 
from hdl_toolkit.interfaces.std import Ap_clk, Ap_rst_n
from hdl_toolkit.synthetisator.shortcuts import toRtl

class Fifo(UnitFromHdl):
    _hdlSources = ["vhdl/fifo.vhd"]
    _intfClasses = [FifoWriter, FifoReader, Ap_clk, Ap_rst_n]


if __name__ == "__main__":
    u = Fifo()
    print(toRtl(u))
    print(u._entity)
