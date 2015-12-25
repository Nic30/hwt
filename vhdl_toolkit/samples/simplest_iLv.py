from vhdl_toolkit.synthetisator.interfaceLevel.synthetizator import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import Ap_none
from vhdl_toolkit.formater import formatVhdl



class SimplestUnit(Unit):
    a = Ap_none(isExtern=True)
    b = Ap_none(src=a, isExtern=True)


if __name__ == "__main__":
    u = SimplestUnit()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise("SimplestUnit")])
                     ))