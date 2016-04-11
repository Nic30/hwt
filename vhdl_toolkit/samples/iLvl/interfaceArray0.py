from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.synthetisator.param import shareAllParams, Param
from vhdl_toolkit.interfaces.std import Ap_vld
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.hdlObjects.typeShortcuts import hInt


@shareAllParams
class InterfaceArraySample(Unit):
    DATA_WIDTH = Param(8)
    a = Ap_vld(multipliedBy=hInt(3), isExtern=True)
    b = Ap_vld(multipliedBy=hInt(3), src=a, isExtern=True)


if __name__ == "__main__":
    print(synthetizeCls(InterfaceArraySample))

