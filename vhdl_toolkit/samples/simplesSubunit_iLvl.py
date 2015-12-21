from vhdl_toolkit.samples.simplest_iLvl import SimplestUnit
from vhdl_toolkit.synthetisator.interfaceLevel.synthetizator import Unit
from vhdl_toolkit.synthetisator.interfaceLevel.stdInterfaces import Ap_none
from vhdl_toolkit.formater import formatVhdl

class SimpleSubunit(Unit):
    subunit0 = SimplestUnit() 
    a = Ap_none(subunit0.a ,isExtern=True)
    b = Ap_none(src=subunit0.b, isExtern=True)

if __name__ == "__main__":
    u = SimpleSubunit()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthetize("SimpleSubunit")])
                     ))