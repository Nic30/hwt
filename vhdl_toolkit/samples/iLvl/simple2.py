from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.param import inheritAllParams, Param


@inheritAllParams
class SimpleUnit2(Unit):
    DATA_WIDTH = Param(8)
    a = AxiStream(isExtern=True)
    b = AxiStream(src=a, isExtern=True)


if __name__ == "__main__":
    u = SimpleUnit2()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))