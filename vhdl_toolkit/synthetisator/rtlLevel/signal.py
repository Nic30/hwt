from vhdl_toolkit.hdlObjects.assigment import Assignment
from vhdl_toolkit.types import VHDLType
from vhdl_toolkit.hdlObjects.variables import SignalItem
from vhdl_toolkit.hdlObjects.operators import Op, InvalidOperandExc
from vhdl_toolkit.hdlObjects.operatorDefinitions import AllOps
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.simExceptions import SimNotInitialized

def checkOperands(ops):
    for op in ops:
        checkOperand(op)

def checkOperand(op):
    if isinstance(op, Value) or isinstance(op, Signal):
        return
    else:
        raise InvalidOperandExc("Operands in hdl expressions can be only instance of Value or Signal,"
                                + "\ngot instance of %s" % (op.__class__))

#[TODO] move to operator definition
class SignalNode():

    @staticmethod
    def resForOp(op):
        t = op.getReturnType() 
        out = Signal(None, t)
        out.drivers.add(op)
        out.origin = op
        op.result = out
        return out

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
        return self.unaryOp(AllOps.NOT)
        
    def opOnRisigEdge(self):
        return self.unaryOp(AllOps.RISING_EDGE)
    
    def opAnd(self, *operands):
        return self.naryOp(AllOps.AND_LOG, operands)

    def opXor(self, *operands):
        return self.naryOp(AllOps.XOR, operands)

    def opOr(self, *operands):
        return self.naryOp(AllOps.OR_LOG, operands)

    def opIsOn(self):
        if self.onIn == 0:
            return self.opNot()
        else:
            return self 
        
    def opEq(self, *operands):
        return self.naryOp(AllOps.EQ, operands)

    def opNEq(self, *operands):
        return self.naryOp(AllOps.NEQ, operands)
    
    def opAdd(self, *operands):
        return self.naryOp(AllOps.PLUS, operands)
    
    def assignFrom(self, source):
        checkOperand(source)
        a = Assignment(source, self)
        a.cond = set()
        self.drivers.add(a)
        if not isinstance(source, Value):
            source.endpoints.add(a)
        return a
    
class Signal(SignalItem, SignalOps):
    """
    more like net
    @ivar _usedOps: dictionary of used operators which can be reused
    """
    def __init__(self, name, var_type, defaultVal=None, onIn=None):
        if name is None:
            name = "sig_" + str(id(self))
            self.hasGenericName = True 
        if onIn == None:
            onIn = Value.fromVal(True, bool)
        assert(isinstance(var_type, VHDLType))  # range, downto, to etc.
        super(Signal, self).__init__(name, var_type, defaultVal)
        self.endpoints = set()
        self.drivers = set()
        assert(isinstance(onIn, Value))
        self.onIn = onIn
        self._usedOps = {}
        
    

    
    def simPropagateChanges(self):
        if self._oldVal != self._val or self._oldVal.eventMask != self._val.eventMask:
            conf = self._simulator.config
            env = self._simulator.env
            self._oldVal = self._val
            for e in self.endpoints:
                if conf.log:
                    conf.logger("%d: Signal.simPropagateChanges %s -> %s" % (env.now, self.name, str(e)))
                yield env.process(e.simPropagateChanges())
        
    
    def simUpdateVal(self, newVal):
        assert(isinstance(newVal, Value))
        self._val = newVal
        try:
            env = self._simulator.env
        except AttributeError:
            raise SimNotInitialized("Singal %s does not contains reference to its simulator" % (str(self)))
        c = self._simulator.config
        if  c.log:
            c.logger("%d: %s <= %s" % (env.now, self.name, str(newVal)))
        
        yield env.process(self.simPropagateChanges())
class SyncSignal(Signal):
    def __init__(self, name, var_type, defaultVal=None):
        super().__init__(name, var_type, defaultVal)
        self.next = Signal(name + "_next", var_type, defaultVal)
        
    def assignFrom(self, source):
        a = Assignment(source, self.next)
        a.cond = set()
        self.next.drivers.add(a)
        if not isinstance(source, Value):
            self.endpoints.add(source)
             
        return a
