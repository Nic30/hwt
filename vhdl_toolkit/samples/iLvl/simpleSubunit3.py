from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.param import Param, inheritAllParams

@inheritAllParams
class SimpleSubunit3(Unit):
    DATA_WIDTH = Param(8)
    subunit0 = SimpleUnit2() 
    a0 = AxiStream(subunit0.a ,isExtern=True)
    b0 = AxiStream(src=subunit0.b, isExtern=True)

if __name__ == "__main__":
    u = SimpleSubunit3()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))