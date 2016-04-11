from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.synthetisator.param import Param, shareAllParams
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls

@shareAllParams
class SimpleSubunit3(Unit):
    DATA_WIDTH = Param(128)
    subunit0 = SimpleUnit2() 
    a0 = AxiStream(subunit0.a ,isExtern=True)
    b0 = AxiStream(src=subunit0.b, isExtern=True)

if __name__ == "__main__":
    print(synthetizeCls(SimpleSubunit3))
