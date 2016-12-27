from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps, isEventDependentOp
from hwt.hdlObjects.portItem import PortItem
from hwt.hdlObjects.constants import DIRECTION, SENSITIVITY
from hwt.hdlObjects.statements import IfContainer, SwitchContainer
from hwt.hdlObjects.value import Value
from hwt.pyUtils.arrayQuery import where
from hwt.synthesizer.param import Param
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc


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
                raise TypeError("walkAllOriginSignals not implemented for %s" % (str(obj)))
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

class EventDependencyReached(Exception):
    """
    Exception which signalize that walkDriversInExpr 
    has reached event dependent operator
    """
    def __init__(self, evOp):
        self.evOp = evOp

def walkDriversInExpr(expr, seenSet):
    """
    @return: generators of RtlSignal
            where signal is in expression and is not used in event dependent expression
    @raise EventDependencyReached: when this generator steps on event dependent operator 
    @attention: if event operator is found in expression, only sensitivity EventDependencyReached is raised
                this may case some synthesis (Vivado, ISE, Quartus ...) to complain about sensitivity, 
                but it will work 
    """
    if isinstance(expr, (Value, Param)):
        pass
    elif isinstance(expr, RtlSignalBase):
        if expr in seenSet:
            pass
        else:
            seenSet.add(expr)
            
            if not expr.hidden:
                yield expr
                return
            
            try:
                op = expr.singleDriver()
            except MultipleDriversExc:
                yield expr
                return
            
            if not isinstance(op, Operator):
                yield expr
                return
            
            if isEventDependentOp(op.operator):
                raise EventDependencyReached(op)
            else:
                for operand in op.ops:
                    yield from walkDriversInExpr(operand, seenSet)
                    
    else:           
        raise TypeError(expr)

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


def isEdgeDependent(sens):
    return sens == SENSITIVITY.RISING or sens == SENSITIVITY.FALLING

def _discoverSensitivity(statement, seenSet, isTop):
    try:
        if isinstance(statement, Assignment):
            if statement.indexes:
                for i in statement.indexes:
                    yield from walkDriversInExpr(i, seenSet)
            yield from walkDriversInExpr(statement.src, seenSet)
        elif isinstance(statement, IfContainer):
            # if true
            for c in statement.cond:
                yield from walkDriversInExpr(c, seenSet)
            for stm in statement.ifTrue:
                yield from _discoverSensitivity(stm, seenSet, False)
            # elifs
            for cond, stms in statement.elIfs:
                for c in cond:
                    yield from walkDriversInExpr(c, seenSet)
                for stm in stms:
                    yield from _discoverSensitivity(stm, seenSet, False)
            # else
            for stm in statement.ifFalse:
                yield from _discoverSensitivity(stm, seenSet, False)
            
        elif isinstance(statement, SwitchContainer):
            yield from walkDriversInExpr(statement.switchOn, seenSet)
            for cond, stms in statement.cases:
                # yield from walkDriversInExpr(cond, seenSet)
                for stm in stms:
                    yield from _discoverSensitivity(stm, seenSet, False)
        else:
            raise TypeError(statement)
        
    except EventDependencyReached as e:
        if isTop:
            yield e.evOp
        else:
            raise e

def discoverSensitivity(statement):
    """
    @return: generators of (sensitivity, signal)
            where sensitivity is member of SENSITIVITY enum
    """
    yield from _discoverSensitivity(statement, set(), True) 
        
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
        
        
