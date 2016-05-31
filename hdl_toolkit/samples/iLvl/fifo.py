from hdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.interfaces.std import Ap_none, Ap_clk, Ap_rst_n
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.synthetisator.shortcuts import toRtl

class FifoWriter(Interface):
    def _config(self):
        self.DATA_WIDTH = Param(8)
        
    def _declr(self):
        self.en = Ap_none()
        self.wait = Ap_none(masterDir=DIRECTION.IN)
        self.data = Ap_none(dtype=vecT(self.DATA_WIDTH), alternativeNames=[''])

class FifoReader(FifoWriter):
    def _declr(self):
        super()._declr()
        self.en._masterDir = DIRECTION.IN
        self.wait._masterDir = DIRECTION.OUT

class Fifo(UnitFromHdl):
    _hdlSources = ["vhdl/fifo.vhd"]
    _intfClasses = [FifoWriter, FifoReader, Ap_clk, Ap_rst_n]



if __name__ == "__main__":
    u = Fifo()
    print(toRtl(u))
    print(u._entity)
