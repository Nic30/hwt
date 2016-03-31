from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls


class SimpleUnit(Unit):
    a = Ap_none(isExtern=True)
    b = Ap_none(src=a, isExtern=True)


if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit))
