from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT, hInt
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls



class SimpleUnit4(Unit):
    DATA_WIDTH = Param(16)
    dtype = vecT(DATA_WIDTH.opDiv(hInt(8)))
    a = Ap_none(dtype=dtype, isExtern=True)
    b = Ap_none(dtype=dtype, src=a, isExtern=True)


if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit4))
