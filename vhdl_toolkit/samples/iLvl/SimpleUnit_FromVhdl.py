from vhdl_toolkit.synthetisator.interfaceLevel.unitFromHdl import UnitFromHdl
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls


class SimpleUnit_FromVhdl(UnitFromHdl):
    _hdlSources = 'vhdl/simplest_b.vhd'

if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit_FromVhdl))
