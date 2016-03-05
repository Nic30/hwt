from python_toolkit.arrayQuery import first, where
from vhdl_toolkit.hdlObjects.assigment import Assignment
from vhdl_toolkit.types import DIRECTION
from vhdl_toolkit.hdlObjects.typeDefinitions import VHDLBoolean 
from vhdl_toolkit.hdlObjects.variables import SignalItem, PortItem
from vhdl_toolkit.interfaces.std import Ap_none
from vhdl_toolkit.synthetisator.param import getParam
from vhdl_toolkit.hdlObjects.operators import Op

class InvalidOperandExc(Exception):
    pass

def checkOperands(ops):
    for op in ops:
        checkOperand(op)

def checkOperand(op):
    if isinstance(op, int) or isinstance(op, Signal):
        return
    else:
        raise InvalidOperandExc()


class SignalNode():

    @staticmethod
    def resForOp(op):
        t = op.getReturnType() 
        out = Signal(None, t)
        out.origin = op
        op.result = out
        return out

def PortItemFromSignal(s):
    if s.hasDriver():
        d = DIRECTION.OUT
    else:
        d = DIRECTION.IN
    pi = PortItem(s.name, d, s.var_type)
    if not hasattr(s, '_interface'):
        w = s.var_type.width
        s._interface = Ap_none(width=w)
        s._interface._width = w
    pi._interface = s._interface
    
    return pi

class PortConnection():
    def __init__(self, signal, unit, portItem):
        self.sig = signal
        self.unit = unit
        self.portItem = portItem
        
    def asPortMap(self):
        p_w = getParam(self.portItem.var_type.getWidth())
        s_w = getParam(self.sig.var_type.getWidth())
        if p_w > s_w:  # if port item is wider fill signal with zeros
            diff = p_w - s_w
            return ('%s => %s & X"' + "%0" + str(diff) + 'd"') % (self.portItem.name, self.sig.name, 0) 
        elif p_w < s_w:  # if signal is wider take lower part
            return '%s => %s( %d downto 0)' % (self.portItem.name, self.sig.name, p_w - 1)
        else:
            return " %s => %s" % (self.portItem.name, self.sig.name)

class SignalOps():
    def unaryOp(self, operator):
        try:
            o = self._usedOps[operator]
            return o.result
        except KeyError:
            o = Op(operator, [self])
            self._usedOps[operator] = o
            return SignalNode.resForOp(o)
    
    def naryOp(self, operator, operands):
        checkOperands(operands)
        operands = list(operands)
        operands.insert(0, self)
        o = Op(operator, operands)
        return SignalNode.resForOp(o)
    
    def opNot(self):
        return self.unaryOp(Op.NOT)
        
    def opOnRisigEdge(self):
        return self.unaryOp(Op.RISING_EDGE)
    
    def opAnd(self, *operands):
        return self.naryOp(Op.AND_LOG, operands)

    def opXor(self, *operands):
        return self.naryOp(Op.XOR, operands)

    def opOr(self, *operands):
        return self.naryOp(Op.OR_LOG, operands)

    def opIsOn(self):
        if int(self.onIn) == 0:
            return self.opNot()
        else:
            return self 
        
    def opEq(self, *operands):
        return self.naryOp(Op.EQ, operands)

    def opNEq(self, *operands):
        return self.naryOp(Op.NEQ, operands)

    def assignFrom(self, source):
        checkOperand(source)
        a = Assignment(source, self)
        a.cond = set()
        self.expr.append(a)
        return a
    
class Signal(SignalItem, SignalOps):
    # more like net
    def __init__(self, name, var_type, defaultVal=None, onIn=True):
        if name is None:
            name = "sig_" + str(id(self))
            self.hasGenericName = True 
        super().__init__(name, var_type, defaultVal)
        self.expr = []
        self.onIn = onIn
        self._usedOps = {}
    
    def connectToPortItem(self, unit, portItem):
        associatedWith = first(unit.portConnections, lambda x: x.portItem == portItem) 
        if associatedWith:
            raise Exception("Port %s is already associated with %s" % (portItem.name, str(associatedWith.sig)))
        e = PortConnection(self, unit, portItem)
        unit.portConnections.append(e)
        self.expr.append(e)
        return e
    
    def hasDriver(self):
        for _ in self.getDrivers():
            return True
        return False
    
    def getDrivers(self):
        def assign2Me(ep):
            if isinstance(ep, Assignment) and ep.dst == self:
                return ep
            elif isinstance(ep, PortConnection) and ep.portItem.direction == DIRECTION.OUT: 
                return ep
            else:
                return None
                
        return where(walkSigExpr(self), assign2Me)
 
class SyncSignal(Signal):
    def __init__(self, name, var_type, defaultVal=None):
        super().__init__(name, var_type, defaultVal)
        self.next = Signal(name + "_next", var_type, defaultVal)
        
    def assignFrom(self, source):
        a = Assignment(source, self.next)
        a.cond = set()
        self.expr.append(a)
        return a
 
def walkSigExpr(sig):
    if hasattr(sig, 'origin'):
        yield sig.origin
    for e in sig.expr:
        yield  e

def walkUnitInputs(unit):
    for pc in unit.portConnections:
        if pc.portItem.direction == DIRECTION.IN:
            yield pc.sig

def walkSignalsInExpr(expr):
    if isinstance(expr, int):
        return
    elif isinstance(expr, Op):
        for op in expr.op:
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
    elif isinstance(sig, Op):
        for op in sig.op:
            if op != parent:
                yield from walkSigSouces(op)
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
        
        
