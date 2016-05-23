from hdl_toolkit.synthetisator.interfaceLevel.interface import Interface
from hdl_toolkit.hdlObjects.typeShortcuts import hInt, vec
from hdl_toolkit.hdlObjects.typeDefs import BIT
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import walkPhysInterfaces
from hdl_toolkit.hdlObjects.vectorUtils import getWidthExpr
from hdl_toolkit.synthetisator.param import Param
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal, SignalNode
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from copy import deepcopy

def _connectSig(src, dst):
    if isinstance(src, Interface):
        if isinstance(dst, Interface):
            if isinstance(dst, Interface):
                dst._src = True
            return dst._connectTo(src)
        
    dst._src = src
    if isinstance(dst, Interface):
        dst._src = src
        dst = dst._sig 
    
    src =  src._dtype.convert(src, dst._dtype)
    
    return [dst._assignFrom(src)]

def connectSig(src, *destinations):
    """
    Connect all signals works with interfaces as well
    """
    assignemnts = []
    for dst in destinations:
        assignemnts.extend(_connectSig(src, dst))
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
                res = res.opConcat(s)
        
    return res

def trim(src, targetWidth):
    return vecWithOffset(src, targetWidth, 0)

def vecWithOffset(src, width, offset):
    """
    Slice out signal of width with offset.
    """
    # [TODO] parametrizable offset
    lower = hInt(offset)
    if isinstance(width, int):
        width = hInt(width)
        
    if isinstance(width, (Param, Signal)):
        upper = width.opAdd(hInt(offset)).opSub(hInt(1))
        r = lower.opDownto(upper)
    else:
        upper = hInt(width.val + offset - 1)
        r = SignalNode.resForOp(Operator(AllOps.DOWNTO, [upper, lower]))
    return src.opSlice(r)

def connectUnpacked(src, dst):
    """src is packed and it is unpacked and connected to dst"""
    # [TODO] parametrized offsets
    if isinstance(src, Interface):
        src = src._sig
    offset = 0
    connections = []
    for i in walkPhysInterfaces(dst):
        sig = i._sig
        t = sig._dtype
        if t == BIT:
            s = src.opSlice(hInt(offset))
            offset += 1
        else:
            w = getWidthExpr(t)
            s = vecWithOffset(src, w, offset)
            offset += t.getBitCnt()
        i._src = s    
        connections.append(sig._assignFrom(s))
    
    return connections
    
def packedWidth(intf):
    """Sum of all width of interfaces in this interface"""
    if isinstance(intf, type):
        # interface class
        intf = intf()
        intf._loadDeclarations()
    elif isinstance(intf, Interface) and not hasattr(intf, "_interfaces"):
        # not loaaded interface
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
        return t.getBitCnt()

def fitTo(what, to):
    """
    Slice signal "what" to fit in "to" 
    or
    extend "what" with zeros to same width as "to"
    
    little endian impl.
    """

    whatWidth = what._dtype.getBitCnt()
    toWidth = to._dtype.getBitCnt()
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
            if isinstance(s, Interface):
                s = s._sig
            if top is None:
                top = s
            else:
                top = fn(top, s)
        return top
    return op

And = mkOp(lambda top, s: top.opAnd(s))
Or = mkOp(lambda top, s: top.opOr(s))
Concat = mkOp(lambda top, s: top.opConcat(s))

