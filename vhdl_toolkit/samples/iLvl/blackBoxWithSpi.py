from vhdl_toolkit.synthetisator.interfaceLevel.emptyUnit import EmptyUnit 
from vhdl_toolkit.interfaces.std import SPI
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls



class EmptyUnitWithSpi(EmptyUnit):
    spi = SPI(isExtern=True)
    
    
if __name__ == "__main__":
    print(synthetizeCls(EmptyUnitWithSpi))
