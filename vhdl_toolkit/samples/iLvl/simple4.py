from vhdl_toolkit.synthetisator.interfaceLevel.unit import Unit
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.formater import formatVhdl
from vhdl_toolkit.synthetisator.param import Param
from vhdl_toolkit.hdlObjects.typeShortcuts import vecT, hInt



class SimpleUnit4(Unit):
    DATA_WIDTH = Param(16)
    a = Ap_none(dtype=vecT(DATA_WIDTH.opDiv(hInt(8))), isExtern=True)
    b = Ap_none(dtype=vecT(DATA_WIDTH.opDiv(hInt(8))), src=a, isExtern=True)


if __name__ == "__main__":
    u = SimpleUnit4()
    print(formatVhdl(
                     "\n".join([ str(x) for x in u._synthesise()])
                     ))