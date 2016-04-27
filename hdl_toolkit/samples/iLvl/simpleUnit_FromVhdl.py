from hdl_toolkit.intfLvl import UnitFromHdl
from hdl_toolkit.synthetisator.shortcuts import synthetizeCls


class SimpleUnit_FromVhdl(UnitFromHdl):
    _hdlSources = 'vhdl/simplest_b.vhd'

if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit_FromVhdl))
