from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls
from vhdl_toolkit.synthetisator.interfaceLevel.interface import connect

class SimpleWithNonDirectIntConncetion(Unit):
    a = Ap_none(isExtern=True)
    b = Ap_none(isExtern=True)
    #c = Ap_none(b, src=a)
    c = connect(a, b)

if __name__ == "__main__":
    print(synthetizeCls(SimpleWithNonDirectIntConncetion))
