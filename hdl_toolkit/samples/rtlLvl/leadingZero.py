
from hdl_toolkit.formater import formatVhdl
from hdl_toolkit.synthetisator.rtlLevel.context import Context
from hdl_toolkit.hdlObjects.typeShortcuts import vecT, vec, hInt, hBit
from hdl_toolkit.synthetisator.rtlLevel.signalUtils import connectSig, trim, \
    Concat, vecWithOffset
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If

w = connectSig


def IndexOps():
    t = vecT(8)
    c = Context("IndexOps")
    
    s_in = c.sig("s_in", t)
    index = c.sig("s_indexOfFirstZero", t)
    
    leadingZeroTop = None  # index is index of first empty record or last one
    for i in reversed(range(8)):
        connections = w(vec(i, 8), index)
        if leadingZeroTop is None:
            leadingZeroTop = connections 
        else:
            leadingZeroTop = If(s_in.opSlice(hInt(i)).opEq(hBit(False)),
               connections
               ,
               leadingZeroTop
            )    
    
    interf = [s_in, index]
    
    return c, interf

if __name__ == "__main__":
    c, interf = IndexOps()
    
    for o in c.synthetize(interf):
            print(formatVhdl(str(o)))

