from vhdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls


class Bram(UnitFromHdl):
    _hdlSources = ["vhdl/dualportRAM.vhd"]
    
if __name__ == "__main__":
    synthetizeCls(Bram)
