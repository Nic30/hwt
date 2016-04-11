from vhdl_toolkit.samples.iLvl.simple import SimpleUnit
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.shortcuts import synthetizeCls

class SimpleSubunit(Unit):
    subunit0 = SimpleUnit() 
    a0 = Ap_none(subunit0.a , isExtern=True)
    b0 = Ap_none(src=subunit0.b, isExtern=True)

if __name__ == "__main__":
    print(synthetizeCls(SimpleSubunit))
