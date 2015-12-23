from vhdl_toolkit.synthetisator.interfaceLevel.synthetizator import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import AxiStream
from vhdl_toolkit.formater import formatVhdl



class SimplestUnit2(Unit):
    a = AxiStream(isExtern=True)
    b = AxiStream(src=a, isExtern=True)


if __name__ == "__main__":
    u = SimplestUnit2()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise("SimplestUnit2")])
                     ))