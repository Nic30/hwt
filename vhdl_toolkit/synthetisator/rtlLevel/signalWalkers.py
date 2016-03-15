from vhdl_toolkit.hdlObjects.specialValues import DIRECTION
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.operators import Operator
from vhdl_toolkit.hdlObjects.portConnection import PortConnection
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
from vhdl_toolkit.hdlObjects.assignment import Assignment
from python_toolkit.arrayQuery import where


def signalHasDriver(sig):
    for _ in walkSignalDrivers(sig):
        return True
    return False

def walkSignalDrivers(sig):
    def assign2Me(ep):
        if isinstance(ep, Assignment) and ep.dst == sig:
            return ep
        elif isinstance(ep, PortConnection) and ep.portItem.direction == DIRECTION.OUT: 
            return ep
        else:
            return None
            
    return where(walkSigExpr(sig), assign2Me)
 
def walkSigExpr(sig):
    """
    Walk any object connected to this signal 
    """
    yield from sig.drivers
    yield from sig.endpoints

def walkUnitInputs(unit):
    for pc in unit.portConnections:
        if pc.portItem.direction == DIRECTION.IN:
            yield pc.sig


def walkAllOriginSignals(sig, discovered=None):
    """
    Walk every signal which has no driver and is used as driver of this signal.
    Goal is walk every generic in static expr. evaluation.
    """
    if discovered is None:
        discovered = set()
    assert(isinstance(sig, Signal))
    if sig in discovered:
        return
    discovered.add(sig)
    
    if sig.drivers:
       
        for obj in sig.drivers:
            if isinstance(obj, Value):
                raise StopIteration()
            elif isinstance(obj, Operator):
                for op in obj.ops:
                    if isinstance(op, Signal):
                        yield from walkAllOriginSignals(op, discovered=discovered)
            elif isinstance(obj, Signal):
                yield from walkAllOriginSignals(obj, discovered)
            elif isinstance(obj, Assignment):
                yield from walkAllOriginSignals(obj.src, discovered)
            else:
                raise NotImplementedError("walkAllOriginSignals not implemented for %s" % (str(obj)))
    else:
        yield sig

def _walkAllRelatedSignals(obj, discovered=None):
    """
    Walk every code element and discover every signal which has any relation to this object 
    (even not direct)
    """
    if isinstance(obj, Value):
        raise StopIteration()
    elif isinstance(obj, Operator):
        for op in obj.ops:
            yield from _walkAllRelatedSignals(op, discovered=discovered)
    elif isinstance(obj, Signal):
        yield from walkAllRelatedSignals(obj, discovered=discovered)
    elif isinstance(obj, Assignment):
        for s in [obj.src, obj.dst]:
            yield from _walkAllRelatedSignals(s, discovered=discovered)
    else:
        raise NotImplementedError("walkAllRelatedSignals not implemented for node %s" % (str(obj)))

        
def walkAllRelatedSignals(sig, discovered=None):
    """
    Walk every code element and discover every signal which has any relation to this signal 
    (even not direct)
    """
    
    if discovered is None:
        discovered = set()
    assert(isinstance(sig, Signal))
    if sig in discovered:
        return

    discovered.add(sig)
    yield sig
    for e in walkSigExpr(sig):
        yield from _walkAllRelatedSignals(e, discovered)
        
def walkSignalsInExpr(expr):
    if isinstance(expr, Value):
        return
    elif isinstance(expr, Operator):
        for op in expr.ops:
            if op != expr:
                yield from walkSignalsInExpr(op)
    elif isinstance(expr, Signal):
        if hasattr(expr, "origin"):
            yield from  walkSignalsInExpr(expr.origin)
        else:
            yield expr
    else:
        raise Exception("Unknown node type %s" % str(expr.__class__))

def discoverSensitivity(datapath):
    if not isinstance(datapath, Assignment):
        raise Exception("Not implemented")
    for c in datapath.cond:
        yield from walkSignalsInExpr(c)
    yield from walkSignalsInExpr(datapath.src)
        
# walks code but do not cross assignment of precursors 
def walkSigSouces(sig, parent=None):    
    if isinstance(sig, int):
        return
    elif isinstance(sig, Operator):
        for op in sig.op:
            if op != parent:
                yield from walkSigSouces(op)
    elif isinstance(sig, Signal):
        if hasattr(sig, 'origin'):  # if this is only internal signal
            yield from walkSigSouces(sig.origin)
        for e in sig.drivers:
            if isinstance(e, PortConnection):
                if not e.unit.discovered:
                    yield e
            elif isinstance(e, Assignment) and e.src != sig:
                yield e
            else:
                yield from walkSigSouces(e, sig)
    else:
        raise Exception("Cant walk node %s" % str(sig))
        
        
