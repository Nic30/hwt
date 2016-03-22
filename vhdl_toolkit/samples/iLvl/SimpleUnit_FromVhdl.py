from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.interfaceLevel.unit import UnitWithSource


class SimpleUnit_FromVhdl(UnitWithSource):
    _hdlSources = 'vhdl/simplest_b.vhd'

if __name__ == "__main__":
    u = SimpleUnit_FromVhdl()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))