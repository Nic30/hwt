from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.defs import Integer, BIT
from hwt.hdlObjects.value import Value
from hwt.hdlObjects.types.sliceVal import SliceVal
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.typeShortcuts import vec

def getWidthExpr(vectorTypeInst):
    c = vectorTypeInst.constrain
    if isinstance(c, SliceVal):
        return c.val[0] + 1
    downto = c.singleDriver()
    
    assert downto.operator == AllOps.DOWNTO
    assert downto.ops[1].val == 0
    
    
    widthMinOne = downto.ops[0]
    if isinstance(widthMinOne, Value) and isinstance(widthMinOne._dtype, Integer):
        w = widthMinOne.clone()
        w.val += 1
        return w
    else:
        widthMinOne = widthMinOne.singleDriver()
    assert widthMinOne.operator == AllOps.SUB
    assert widthMinOne.ops[1].val == 1
    
    return widthMinOne.ops[0]

def aplyIndexOnSignal(sig, dstType, index):
    if sig._dtype == BIT or dstType == BIT:
        return sig[index]
    elif isinstance(dstType, Bits):
        w = getWidthExpr(dstType)
        return sig[(w * (index + 1)):(w * index)]
    else:
        raise NotImplementedError()

def fitTo(what, to):
    """
    Slice signal "what" to fit in "to" 
    or
    extend "what" with zeros to same width as "to"
    
    little-endian impl.
    """

    whatWidth = what._dtype.bit_length()
    toWidth = to._dtype.bit_length()
    if toWidth == whatWidth:
        return what
    elif toWidth < whatWidth:
        # slice
        return what[toWidth:]
    else:
        # extend
        return vec(0, toWidth - whatWidth)._concat(what)