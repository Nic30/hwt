from vhdl_toolkit.synthetisator.interfaceLevel.synthetizator import Unit
from vhdl_toolkit.formater import formatVhdl


class SimpleUnit_b(Unit):
    _origin = 'vhdl/simplest_b.vhd'

if __name__ == "__main__":
    u = SimpleUnit_b()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))