from vhdl_toolkit.samples.iLvl.simple2 import SimpleUnit2
from vhdl_toolkit.synthetisator.interfaceLevel.synthetizator import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import AxiStream
from vhdl_toolkit.formater import formatVhdl

class SimpleSubunit2(Unit):
    subunit0 = SimpleUnit2() 
    a0 = AxiStream(subunit0.a ,isExtern=True)
    b0 = AxiStream(src=subunit0.b, isExtern=True)

if __name__ == "__main__":
    u = SimpleSubunit2()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))