from hdl_toolkit.interfaces.std import Clk, s, D, Signal
from hdl_toolkit.synthesizer.interfaceLevel.interface import Interface
from hdl_toolkit.interfaces.tristate import TristateClk, TristateSig

class Spi(Interface):
    def _declr(self):
        self.clk = Clk()
        self.mosi = s()              # master out slave in
        self.miso = s(masterDir=D.IN)# master in slave out
        self.cs = s()                # chip select

class I2c(Interface):
    def _declr(self):
        self.slc = TristateClk() # clk
        self.sda = TristateSig() # data

class Uart(Interface):
    def _declr(self):
        self.rx = Signal(masterDir=D.IN)
        self.tx = Signal()