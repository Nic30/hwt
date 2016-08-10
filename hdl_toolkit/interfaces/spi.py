from hdl_toolkit.interfaces.std import Clk, s, D
from hdl_toolkit.synthesizer.interfaceLevel.interface import Interface


class SPI(Interface):
    def _declr(self):
        self.clk = Clk()
        self.mosi = s()              # master out slave in
        self.miso = s(masterDir=D.IN)# master in slave out
        self.cs = s()                # chip select