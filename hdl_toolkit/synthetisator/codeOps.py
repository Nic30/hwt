from copy import deepcopy
from hdl_toolkit.hdlObjects.typeShortcuts import hInt, vec
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import walkPhysInterfaces
from hdl_toolkit.hdlObjects.vectorUtils import getWidthExpr
from hdl_toolkit.hdlObjects.specialValues import DIRECTION


def _intfToSig(obj):
    if isinstance(obj, InterfaceBase):
        return obj._sig
    else:
        return obj

def If(cond, ifTrue=[], ifFalse=[]):
    """
    Create if statement
    """
    cond = _intfToSig(cond)
    
    for stm in ifTrue:
        cond.endpoints.append(stm)
        stm.cond.add(cond)
    
    if ifFalse:
        # to prevent creating ~cond without reason
        ncond = ~cond
        for stm in ifFalse:
            ncond.endpoints.append(stm)
            stm.cond.add(ncond)
    
    ret = []
    ret.extend(ifTrue)
    ret.extend(ifFalse)
    return ret

def Switch(val, *cases):
    """
    Create switch statement
    """
    top = None
    for c in reversed(cases):
        if top is None:
            top = c[1]
        else:
            assert c[0] is not None
            top = If(val._eq(c[0]),
                     c[1]
                     ,
                     top
                    )
    return top

def genTransitions(st, *transitions):
    """
    @param st: variable which is driven by actual transition
    @param transitions: tupes (condition, newvalue)
    
    @attention: transitions has priority, first has the biggest 
    """
    top = st._same()
    
    for condition, newvalue in reversed(transitions):
        top = If(condition,
                    c(newvalue, st)
                    ,
                    top
                )
        
    return top

def _connect(src, dst, srcExclude, dstExclude):
    if srcExclude or dstExclude:
        raise NotImplementedError("[TODO]")
        
    if isinstance(src, InterfaceBase):
        if isinstance(dst, InterfaceBase):
            return dst._connectTo(src)
        src = src._sig
        
    src = toHVal(src)
    src = src._dtype.convert(src, dst._dtype)
    
    return [dst._assignFrom(src)]

def connect(src, *destinations, srcExclude=[], dstExclude=[]):
    """
    Connect all signals/interfaces/calues
    """
    assignemnts = []
    for dst in destinations:
        assignemnts.extend(_connect(src, dst, srcExclude, dstExclude))
    return assignemnts

def packed(intf, masterDirEqTo=DIRECTION.OUT, exclude=set()):
    """
    Concatenate all signals to one big signal, recursively
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
            s = src[(w+offset): offset]
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
        return what[:hInt(toWidth)]
    else:
        # extend
        return Concat(what, vec(0, toWidth - whatWidth))
       

def _mkOp(fn): 
    def op(*ops):
        top = None 
        for s in ops:
            if top is None:
                top = s
            else:
                top = fn(top, s)
        return top
    return op

And = _mkOp(lambda top, s: top & s)
Or = _mkOp(lambda top, s: top | s)
Concat = _mkOp(lambda top, s: top._concat(s))

c = connect