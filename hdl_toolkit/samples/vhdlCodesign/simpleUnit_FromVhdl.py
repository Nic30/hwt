from hdl_toolkit.intfLvl import UnitFromHdl

class SimpleUnit_FromVhdl(UnitFromHdl):
    _hdlSources = 'vhdl/simplest_b.vhd'

if __name__ == "__main__":
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    print(toRtl(SimpleUnit_FromVhdl))
