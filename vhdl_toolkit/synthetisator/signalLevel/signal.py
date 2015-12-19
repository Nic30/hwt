from python_toolkit.arrayQuery import arr_any, single, first
from vhdl_toolkit.expr import Assignment, value2vhdlformat
from vhdl_toolkit.types import VHDLType, VHDLBoolean, DIRECTION
from vhdl_toolkit.variables import SignalItem, PortItem


class InvalidOperandExc(Exception):
    pass

def checkOperand(op):
    if isinstance(op, int) or isinstance(op, Signal):
        return
    else:
        raise InvalidOperandExc()

def exp__str__(dst, src):
    if isinstance(src, OperatorUnary) or isinstance(src, OperatorBinary):
        return "(" + str(src) + ")"
    elif isinstance(src, Signal) and hasattr(src, 'origin'):
        return exp__str__(dst, src.origin)  # consume signal between operators
    else:
        return value2vhdlformat(dst, src)

def assigmet__str__(self):
    return "%s <= %s" % (self.dst.name, exp__str__(self.dst, self.src))
Assignment.__str__ = assigmet__str__  


class OperatorUnary:
    def __init__(self, operand):
        self.operand = operand
        self.result = Signal(None, operand.var_type)
        self.result.origin = self
        
class OpOnRisingEdge(OperatorUnary):
    def __str__(self):
        return "RISING_EDGE(" + exp__str__(self.result, self.operand) + ")"
    
class OpEvent(OperatorUnary):
    def __str__(self):
        return exp__str__(self.result, self.operand) + "'EVENT"

class OpNot(OperatorUnary):
    def __str__(self):
        return " NOT(" + exp__str__(self.result, self.operand) + ")"

class BitRange(OperatorUnary):
    def __init__(self, signal, down, up):
        self.operand = signal
        self.sig = signal
        self.down = down
        self.up = up
        self.result = Signal(signal.name + "[%d:%d]" % (down, up))
        self.result.origin = self

class OperatorBinary:
    def __init__(self, operand0, operand1):
        self.operand0 = operand0
        self.operand1 = operand1
    def __str__(self):
        return "%s %s %s" % (exp__str__(self.result, self.operand0), self.mark, exp__str__(self.result, self.operand1)) 
        
class OperatorBinaryLogic(OperatorBinary):
    def __init__(self, operand0, operand1):
        super().__init__(operand0, operand1)
        self.result = Signal(None, VHDLBoolean())
        self.result.origin = self

class OpIndx(OperatorBinary):
    def __init__(self, arr, index):
        self.operand0 = arr
        self.operand1 = index

class OpAnd(OperatorBinaryLogic):
    mark = "AND"

class OpOr(OperatorBinaryLogic):
    mark = "OR"

class OpXor(OperatorBinaryLogic):
    mark = "XOR"

class OpEq(OperatorBinaryLogic):
    mark = "="
    
class OpNEq(OperatorBinaryLogic):
    mark = "/="

class OpPlus(OperatorBinary):
    mark = "+"

class OpMinus():
    mark = "1"

def PortItemFromSignal(s):
    if s.hasDriver():
        d = DIRECTION.OUT
    else:
        d = DIRECTION.IN
    pi = PortItem(s.name, d , s.var_type)
    pi.sig = s
    return pi

class PortConnection():
    def __init__(self, signal, unit, portItem):
        self.sig = signal
        self.unit = unit
        self.portItem = portItem
        
    def asPortMap(self):
        p_w = self.portItem.var_type.width
        s_w = self.sig.var_type.width
        if p_w > s_w:  # if port item is wider fill signal with zeros
            diff = p_w - s_w
            return '%s => %s & X"' + "%0" + str(diff) + 'd"' % (self.portItem.name, self.sig.name, 0) 
        elif p_w < s_w:  # if signal is wider take lower part
            return '%s => %s( %d downto 0)' % (self.portItem.name, self.sig.name, p_w - 1)
        else:
            return " %s => %s" % (self.portItem.name, self.sig.name)

#more like net
class Signal(SignalItem):
    def __init__(self, name, var_type, defaultVal=None, onIn=True):
        if name is None:
            name = "sig" + str(id(self))
            self.hasGenericName = True 
        super().__init__(name, var_type, defaultVal)
        self.expr = []
        self.onIn = onIn
    
    def bitRange(self, down, up):
        e = BitRange(self, down, up)
        self.expr.append(e)
        return e.sigSelect
    
    def connectToPortByName(self, unit, name):
        portItem = single(unit.port, lambda x: x.name == name)
        return self.connectToPortItem(unit, portItem)
        
    def connectToPortItem(self, unit, portItem):
        associatedWith = first(unit.portConnections, lambda x: x.portItem == portItem) 
        if associatedWith:
            raise Exception("Port %s is already associated with %s" % (portItem.name, str(associatedWith.sig)))
        e = PortConnection(self, unit, portItem)
        unit.portConnections.append(e)
        self.expr.append(e)
        return e
    
    def opEvent(self):
        op = OpEvent(self)
        self.expr.append(op)
        return op.result
    
    def opNot(self):
        if hasattr(self, "_not"):
            return self._not.result
        op = OpNot(self)
        self._not = op
        self.expr.append(op)
        return op.result
    
    def opOnRisigEdge(self):
        if hasattr(self, "_onRisingEdge"):
            return self._onRisingEdge
        
        op = OpOnRisingEdge(self)
        self._onRisingEdge = op
        self.expr.append(op)
        return op
    
    def opAnd(self, operand1):
        checkOperand(operand1)
        op = OpAnd(self, operand1)
        self.expr.append(op)
        return op.result
    def opXor(self, operand1):
        checkOperand(operand1)
        op = OpXor(self, operand1)
        self.expr.append(op)
        return op.result
    def opOr(self, operand1):
        checkOperand(operand1)
        op = OpOr(self, operand1)
        self.expr.append(op)
        return op.result
        
    def opIsOn(self):
        if int(self.onIn) == 0:
            return self.opNot()
        else:
            return self 
            
    def opEq(self, operand1):
        checkOperand(operand1)
        if self.var_type.width == 1:
            # And(Or(Not(a), b), Or(Not(b), a))
            if isinstance(operand1, Signal):
                op1NotOrSelf = operand1.opNot().opOr(self)
            else:
                op1NotOrSelf = self.opOr(not operand1)
            return self.opNot().opOr(operand1).opAnd(op1NotOrSelf)
        else:
            op = OpEq(self, operand1)
            self.expr.append(op)
            return op.result
    
    def opNEq(self, operand1):
        return self.opEq(operand1).opNot()
        
    def indx(self, indexer):
        checkOperand(indexer)
        indx = OpIndx(self, indexer)
        self.expr.append(indx)
        return indx.result
    
    def hasDriver(self):
        return self.getDriver() != None
    
    def getDriver(self):
        def assign2Me(ep):
            if isinstance(ep, Assignment) and ep.dst == self:
                return ep
            elif isinstance(ep, PortConnection) and ep.portItem.direction == DIRECTION.OUT: 
                return ep
            elif isinstance(ep, BitRange) and ep.sigSelect.hasDriver():
                return ep
            else:
                return None
                
        return first(walkSigExpr(self), assign2Me)
    
    def assignFrom(self, source):
        checkOperand(source)
        a = Assignment(source, self)
        a.cond = set()
        self.expr.append(a)
        return a
    
    def toJson(self):
        return {"name": self.name}
 
class SyncSignal(Signal):
    def __init__(self, name, var_type, defaultVal=None):
        super().__init__(name, var_type, defaultVal)
        self.next = Signal(name + "_next", var_type, defaultVal)
        
    def assignFrom(self, source):
        a = Assignment(source, self.next)
        a.cond = set()
        self.expr.append(a)
        return a

 
def ifConfig2Signal(context, ifc, prefix):
    return context.sig(prefix + ifc.phyName, ifc.width)

def signalsForInterface(context, interf, prefix=""):
    sigs = []
    for ifc in interf.port:
        sigs.append(ifConfig2Signal(context, ifc, prefix))
    return sigs   

def walkSigExpr(sig):
    if hasattr(sig, 'originin'):
        yield sig.originin
    for e in sig.expr:
        yield  e

def walkUnitInputs(unit):
    for pc in unit.portConnections:
        if pc.portItem.direction == DIRECTION.IN:
            yield pc.sig

def walkSignalsInExpr(expr):
    if isinstance(expr, int):
        return
    elif isinstance(expr, OperatorBinary):
        yield from walkSignalsInExpr(expr.operand0)
        yield from walkSignalsInExpr(expr.operand1)
    elif isinstance(expr, OperatorUnary):
        if expr.operand == expr.result:
            return
        else:
            yield from walkSignalsInExpr(expr.operand)
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
    elif isinstance(sig, OperatorBinary):
        if sig.operand0 != parent:
            yield from walkSigSouces(sig.operand0)
        if sig.operand1 != parent:    
            yield from walkSigSouces(sig.operand1)
    elif isinstance(sig, OperatorUnary):
        if sig.operand == sig.result:
            return
        else:
            yield from walkSigSouces(sig.operand)
    elif isinstance(sig, Signal):
        if hasattr(sig, 'origin'):  # if this is only internal signal
            yield from walkSigSouces(sig.origin)
        for e in sig.expr:
            if isinstance(e, PortConnection):
                if not e.unit.discovered:
                    yield e
            elif isinstance(e, Assignment) and e.src != sig:
                yield e
            else:
                yield from walkSigSouces(e, sig)

    else:
        raise Exception("Cant walk node %s" % str(sig))
        
        
