from hdl_toolkit.intfLvl import EmptyUnit 
from hdl_toolkit.interfaces.std import SPI
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls



class EmptyUnitWithSpi(EmptyUnit):
    def _declr(self):
        self.spi = SPI(isExtern=True)
    
    
if __name__ == "__main__":
    print(synthetizeCls(EmptyUnitWithSpi))
