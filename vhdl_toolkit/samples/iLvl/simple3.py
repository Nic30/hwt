from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls



class SimpleUnit3(Unit):
    DATA_WIDTH = Param(8)
    a = Ap_none(dtype=vecT(DATA_WIDTH), isExtern=True)
    b = Ap_none(dtype=vecT(DATA_WIDTH), src=a, isExtern=True)


if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit3))
