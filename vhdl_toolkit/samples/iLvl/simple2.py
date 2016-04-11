from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.synthetisator.param import shareAllParams, Param
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls


@shareAllParams
class SimpleUnit2(Unit):
    DATA_WIDTH = Param(8)
    a = AxiStream(isExtern=True)
    b = AxiStream(src=a, isExtern=True)


if __name__ == "__main__":
    print(synthetizeCls(SimpleUnit2))
