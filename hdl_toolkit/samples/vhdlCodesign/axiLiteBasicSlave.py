from hdl_toolkit.intfLvl import UnitFromHdl

class AxiLiteBasicSlave(UnitFromHdl):
    _hdlSources = "vhdl/axiLite_basic_slave.vhd"
    
if __name__ == "__main__":
    from hdl_toolkit.synthetisator.shortcuts import toRtl
    u = AxiLiteBasicSlave()
    print(toRtl(u))
    