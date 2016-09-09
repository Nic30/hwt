from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps, isEventDependentOp
from hdl_toolkit.hdlObjects.portItem import PortItem
from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.synthesizer.param import Param
from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlSignalBase
from python_toolkit.arrayQuery import where


def signalHasDriver(sig):
    for _ in walkSignalDrivers(sig):
        return True
    return False

def walkSignalDrivers(sig):
    def assign2Me(ep):
        if isinstance(ep, Assignment):
            return True
        elif isinstance(ep, PortItem) and ep.dst is sig: 
            return True
        else:
            return None
            
    return where(sig.drivers, assign2Me)
 
def walkSigExpr(sig):
    """
    Walk any object connected to this signal 
    """
    yield from sig.drivers
    yield from sig.endpoints

def walkUnitInputPorts(unit):
    for portItem in unit.ports:
        if portItem.direction == DIRECTION.IN:
            yield portItem


def walkAllOriginSignals(sig, discovered=None):
    """
    Walk every signal which has no driver and is used as driver of this signal.
    Goal is walk every generic in static expr. evaluation.
    """
    if discovered is None:
        discovered = set()
    if isinstance(sig, Value):
        raise StopIteration()
    if not isinstance(sig, RtlSignalBase):
        raise  AssertionError("Expected only instances of signal, got: %s" % 
                              (repr(sig)))
    if sig in discovered:
        return
    discovered.add(sig)
    
    if sig.drivers:
       
        for obj in sig.drivers:
            if isinstance(obj, Value):
                raise StopIteration()
            elif isinstance(obj, Operator):
                for op in obj.ops:
                    if isinstance(op, RtlSignalBase):
                        yield from walkAllOriginSignals(op, discovered=discovered)
            elif isinstance(obj, RtlSignalBase):
                yield from walkAllOriginSignals(obj, discovered)
            elif isinstance(obj, Assignment):
                yield from walkAllOriginSignals(obj.src, discovered)
            else:
                raise NotImplementedError("walkAllOriginSignals not implemented for %s" % (str(obj)))
    else:
        yield sig

def walkSignalsInExpr(expr):
    if isinstance(expr, Value):
        return
    elif isinstance(expr, Operator):
        for op in expr.ops:
            if op is not expr:
                yield from walkSignalsInExpr(op)
    elif isinstance(expr, RtlSignalBase):
        if hasattr(expr, "origin"):
            yield from  walkSignalsInExpr(expr.origin)
        else:
            yield expr
    else:
        raise Exception("Unknown node '%s' type %s" % 
                        (repr(expr), str(expr.__class__)))

def discoverEventDependency(sig):
    """
    walk signals drivers and yields whose signals which are in some event operator
    """
    try:
        drivers = sig.drivers
    except AttributeError:
        return
    
    if len(drivers) == 1:
        d = drivers[0]
        if isinstance(d, Operator):
            if isEventDependentOp(d.operator):
                yield d.ops[0]
            else:
                for op in d.ops:
                    yield from discoverEventDependency(op)


def discoverDriverSignals(datapath):
    """
    @return: generators of (isSensitive, signal)
    """
    # [TODO] resolve signals and event dependency in once
    
    if not isinstance(datapath, Assignment):
        raise NotImplementedError()
    
    eventDependency = set()
    for c in datapath.cond:
        for ed in discoverEventDependency(c):
            eventDependency.add(ed)

    for c in datapath.cond:
        for s in walkSignalsInExpr(c):
            if not isinstance(s, Param):
                yield (s in eventDependency, s)
                
    for s in walkSignalsInExpr(datapath.src):
            if not isinstance(s, Param):
                yield (s in eventDependency, s)
        
# walks code, and returns assignments and port items which are driving this signal
def walkSigSouces(sig, parent=None):    
    if isinstance(sig, Operator):
        if sig.operator != AllOps.INDEX:  # [TODO] more test to assert this cond. will work
            for op in sig.ops:
                if not op is parent:
                    yield from walkSigSouces(op)
    elif isinstance(sig, RtlSignalBase):
        for e in sig.drivers:
            if isinstance(e, PortItem):
                if not e.unit.discovered:
                    yield e
            elif isinstance(e, Assignment) and not e.src is sig:
                yield e
            else:
                yield from walkSigSouces(e, sig)
    else:
        raise Exception("Cant walk node %s" % repr(sig))
        
        
