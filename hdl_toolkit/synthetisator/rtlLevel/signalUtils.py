from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.hdlObjects.typeShortcuts import hBit
from hdl_toolkit.hdlObjects.typeDefs import BOOL, BIT

def connectSig(a, b):
    if isinstance(a, Interface):
        a = a._sig
    b._src = a
    if isinstance(b, Interface):
        b = b._sig 
    
    if isinstance(b, Interface):
        bDtype = b._dtype
    else:
        bDtype = b.dtype
        
    if a.dtype == BOOL and bDtype == BIT:
        return connectBool2Log(a, b)
    else:
        return [b.assignFrom(a)]

def connectBool2Log(a, b):
    assert(a.dtype == BOOL)
    return If(a,
       [b.assignFrom(hBit(1)) ],
       [b.assignFrom(hBit(0)) ]
       )
