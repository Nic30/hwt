from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.formater import formatVhdl



class SimpleWithNonDirectIntConncetion(Unit):
    a = Ap_none(isExtern=True)
    b = Ap_none(isExtern=True)
    c = Ap_none(b, src=a)

if __name__ == "__main__":
    u = SimpleWithNonDirectIntConncetion()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))