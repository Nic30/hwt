from vhdl_toolkit.samples.iLvl.simple import SimpleUnit
from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.formater import formatVhdl

class SimpleSubunit(Unit):
    subunit0 = SimpleUnit() 
    a0 = Ap_none(subunit0.a , isExtern=True)
    b0 = Ap_none(src=subunit0.b, isExtern=True)

if __name__ == "__main__":
    u = SimpleSubunit()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))
