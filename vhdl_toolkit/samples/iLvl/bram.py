from vhdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.interfaces.std import BramPort


class Bram(UnitFromHdl):
    _hdlSources = ["vhdl/dualportRAM.vhd"]
    _intfClasses=[BramPort]
    
if __name__ == "__main__":
    print(synthetizeCls(Bram))
