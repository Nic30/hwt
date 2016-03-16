from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.amba import AxiStream
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.param import inheritAllParams, Param


@inheritAllParams
class simple2withNonDirectIntConnection(Unit):
    DATA_WIDTH = Param(8)
    a = AxiStream(isExtern=True)
    c = AxiStream(isExtern=True)
    b = AxiStream(c, src=a)
    
if __name__ == "__main__":
    u = simple2withNonDirectIntConnection()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))
