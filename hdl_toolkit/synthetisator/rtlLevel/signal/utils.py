from copy import deepcopy
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.hdlObjects.typeShortcuts import hInt, vec
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import walkPhysInterfaces
from hdl_toolkit.hdlObjects.vectorUtils import getWidthExpr
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.typeCast import toHVal


def _connect(src, dst, srcExclude, dstExclude):
    if srcExclude or dstExclude:
        raise NotImplementedError("[TODO]")
        
    if isinstance(src, InterfaceBase):
        if isinstance(dst, InterfaceBase):
            return dst._connectTo(src)
        src = src._sig
        
    src = src._dtype.convert(src, dst._dtype)
    
    return [dst._assignFrom(src)]

def connect(src, *destinations, srcExclude=[], dstExclude=[]):
    """
    Connect all signals works with interfaces as well
    """
    assignemnts = []
    for dst in destinations:
        assignemnts.extend(_connect(src, dst, srcExclude, dstExclude))
    return assignemnts

def packed(intf, masterDirEqTo=DIRECTION.OUT, exclude=set()):
    """
    Concatenate all signals to one big signal
    """
    if not intf._interfaces:
        if intf._masterDir == masterDirEqTo:
            return intf._sig
        return None
    
    res = None
    for i in intf._interfaces:
        if i in exclude:
            continue
        
        if i._interfaces:
            if i._masterDir == DIRECTION.IN:
                d = DIRECTION.oposite(masterDirEqTo)
            else:
                d = masterDirEqTo
            s = packed(i, d, exclude=exclude) 
        else:
            if i._masterDir == masterDirEqTo:
                s = i._sig
            else:
                s = None
        
        if s is not None:
            if res is None:
                res = s
            else:
                res = Concat(res, s)
        
    return res

def trim(src, targetWidth):
    return vecWithOffset(src, targetWidth, 0)

def vecWithOffset(src, width, offset):
    """
    Slice out signal of width with offset.
    """
    # [TODO] parametrizable offset
    lower = toHVal(offset)
    width = toHVal(width)
    upper = width + hInt(offset) - hInt(1)

    return src[upper:lower]

def connectUnpacked(src, dst, exclude=[]):
    """src is packed and it is unpacked and connected to dst"""
    # [TODO] parametrized offsets
    offset = 0
    connections = []
    for i in walkPhysInterfaces(dst):
        if i in exclude:
            continue
        sig = i._sig
        t = sig._dtype
        if t == BIT:
            s = src[hInt(offset)]
            offset += 1
        else:
            w = getWidthExpr(t)
            s = vecWithOffset(src, w, offset)
            offset += t.bit_length()
        connections.append(sig._assignFrom(s))
    
    return connections
    
def packedWidth(intf):
    """Sum of all width of interfaces in this interface"""
    if isinstance(intf, type):
        # interface class
        intf = intf()
        intf._loadDeclarations()
    elif isinstance(intf, InterfaceBase) and not hasattr(intf, "_interfaces"):
        # not loaded interface
        intf = deepcopy(intf)
        intf._loadDeclarations()
        
    
    if intf._interfaces:
        w = 0
        for i in intf._interfaces:
            w += packedWidth(i)
        return w
    else:
        t = intf._dtype
        if t == BIT:
            return 1
        return t.bit_length()

def fitTo(what, to):
    """
    Slice signal "what" to fit in "to" 
    or
    extend "what" with zeros to same width as "to"
    
    little endian impl.
    """

    whatWidth = what._dtype.bit_length()
    toWidth = to._dtype.bit_length()
    if toWidth == whatWidth:
        return what
    elif toWidth < whatWidth:
        # slice
        return vecWithOffset(what, hInt(toWidth), 0)
    else:
        # extend
        return Concat(what, vec(0, toWidth - whatWidth))
       

def mkOp(fn): 
    def op(*ops):
        top = None 
        for s in ops:
            if top is None:
                top = s
            else:
                top = fn(top, s)
        return top
    return op

# [TODO] rm duplications
def indexRange(width, index):
    width = toHVal(width)
    index = toHVal(index)
    upper = width * index
    lower = width * (index + 1) - 1
    return lower._downto(upper)

def aplyIndexOnSignal(sig, dstType, index):
    if sig._dtype == BIT or dstType == BIT:
        return sig[hInt(index)]
    elif isinstance(dstType, Bits):
        w = getWidthExpr(dstType)
        r = indexRange(w, index)
        return sig[r]
    else:
        raise NotImplementedError()


And = mkOp(lambda top, s: top & s)
Or = mkOp(lambda top, s: top | s)
Concat = mkOp(lambda top, s: top._concat(s))

