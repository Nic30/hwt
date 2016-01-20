from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.interfaces.std import Ap_none
from vhdl_toolkit.formater import formatVhdl



class SimpleUnit(Unit):
    a = Ap_none(isExtern=True)
    b = Ap_none(src=a, isExtern=True)


if __name__ == "__main__":
    u = SimpleUnit()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise("SimpleUnit")])
                     ))