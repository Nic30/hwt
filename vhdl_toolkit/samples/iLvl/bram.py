from vhdl_toolkit.synthetisator.interfaceLevel.unit import UnitWithSource
from vhdl_toolkit.formater import formatVhdl

class Bram(UnitWithSource):
    _origin = "vhdl/dualportRAM.vhd"
    
if __name__ == "__main__":
    u = Bram()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))
