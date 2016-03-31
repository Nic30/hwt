from vhdl_toolkit.synthetisator.interfaceLevel.unit import BlackBox
from vhdl_toolkit.interfaces.std import SPI
from vhdl_toolkit.formater import formatVhdl



class BlackBoxWithSpi(BlackBox):
    spi = SPI(isExtern=True)
    
    
if __name__ == "__main__":
    u = BlackBoxWithSpi()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))