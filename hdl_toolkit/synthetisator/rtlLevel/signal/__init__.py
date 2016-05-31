from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.hdlObjects.types import HdlType
from hdl_toolkit.hdlObjects.variables import SignalItem
from hdl_toolkit.hdlObjects.operator import Operator, InvalidOperandExc
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.simulator.exceptions import SimNotInitialized, SimException
from hdl_toolkit.hdlObjects.typeDefs import BOOL, INT, STR
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase

class MultipleDriversExc(Exception):
    pass

defaultConversions = {int: INT,
                      str: STR,
                      bool: BOOL}
def toHVal(op):
    """Convert python value object to object of hdl type value"""
    if isinstance(op, Value) or isinstance(op, Signal):
        return op
    elif isinstance(op, InterfaceBase):
        return op._sig
    else:
        try:
            hType = defaultConversions[type(op)]
        except KeyError:
            hType = None
        
        if hType is None:
            raise TypeError("%s" % (op.__class__))
        return  Value.fromPyVal(op, hType)
    
def checkOperands(ops):
    _ops = []
    for op in ops:
        _ops.append(checkOperand(op))
    return _ops

def checkOperand(op):
    return toHVal(op)
            

class UniqList(list):
    def append(self, obj):
        if obj in self:
            pass
        return list.append(self, obj)

# [TODO] move to Operator, problem with reference Signal/Operator -> signal and operators have to be separated
class SignalNode():

    @staticmethod
    def resForOp(op):
        t = op.getReturnType() 
        out = Signal(None, t)
        out.drivers.append(op)
        out.origin = op
        op.result = out
        return out

class SignalOps():
    def unaryOp(self, operator):
        try:
            o = self._usedOps[operator]
            return o.result
        except KeyError:
            o = Operator(operator, [self])
            self._usedOps[operator] = o
        
            return SignalNode.resForOp(o)
    
    def naryOp(self, operator, operands):
        operands = checkOperands(operands)
        operands.insert(0, self)
        o = Operator(operator, operands)
        
        return SignalNode.resForOp(o)
    
    def __invert__(self):
        return self.unaryOp(AllOps.NOT)
        
    def _onRisingEdge(self):
        return self.unaryOp(AllOps.RISING_EDGE)
    
    def _isOn(self):
        return self._dtype.convert(self, BOOL)
        
    def __and__(self, *operands):
        return self.naryOp(AllOps.AND_LOG, operands)
    
    def __xor__(self, *operands):
        return self.naryOp(AllOps.XOR, operands)

    def __or__(self, *operands):
        return self.naryOp(AllOps.OR_LOG, operands)

    def _eq(self, *operands):
        """Eq is not overloaded because it will destroy hashability of object"""
        return self.naryOp(AllOps.EQ, operands)

    def __ne__(self, *operands):
        return self.naryOp(AllOps.NEQ, operands)
    
    def __add__(self, *operands):
        return self.naryOp(AllOps.PLUS, operands)
    
    def __sub__(self, *operands):
        return self.naryOp(AllOps.MINUS, operands)
    
    def __mul__(self, *operands):
        return self.naryOp(AllOps.MUL, operands)

    def __floordiv__(self, divider):
        return self.naryOp(AllOps.DIV, [divider])
    
    def _downto(self, to):
        return self.naryOp(AllOps.DOWNTO, [to])
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            if key.step is not None or key.start is None or key.stop is None:
                raise NotImplementedError()
            
            # [TODO] endianity current impl. for litle endian only
            stop = toHVal(key.stop)
            start = toHVal(key.start)
            
            key = SignalNode.resForOp(Operator(AllOps.DOWNTO, [start - Value.fromPyVal(1, INT), stop]))
        
        return self._slice(key)
    
    def _slice(self, index):
        return self.naryOp(AllOps.INDEX, [index])
    
    def _concat(self, *operands):
        return self.naryOp(AllOps.CONCAT, operands)
    
    def _ternary(self, ifTrue, ifFalse):
        return self.naryOp(AllOps.TERNARY, (ifTrue, ifFalse))
    
    def _assignFrom(self, source):
        source = checkOperand(source)
        a = Assignment(source, self)
        a.cond = set()
        try:
            # now I am result of the index  self[xx] <= source
            # get index op
            d = self.singleDriver()
            if isinstance(d, Operator) and d.operator == AllOps.INDEX:
                # get singla on which is signal applied
                indexedOn = d.ops[0]
                if isinstance(indexedOn, Signal):
                    # change direction of index for me and for indexed on
                    # print(d, 'to driver of', indexedOn)
                    indexedOn.endpoints.remove(d)
                    indexedOn.drivers.append(d)
                     
                    # print(d, "to endpoint of")    
                    self.drivers.remove(d)
                    self.endpoints.append(d)
        except MultipleDriversExc:
            pass
        
        self.drivers.append(a)
        if not isinstance(source, Value):
            source.endpoints.append(a)
        
        return a
    
    
class Signal(SignalItem, SignalOps):
    """
    more like net
    @ivar _usedOps: dictionary of used operators which can be reused
    """
    def __init__(self, name, dtype, defaultVal=None):
        if name is None:
            name = "sig_" + str(id(self))
            self.hasGenericName = True 
       
        assert(isinstance(dtype, HdlType))  # == can be range, downto, to etc.
        super(Signal, self).__init__(name, dtype, defaultVal)
        # set can not be used because hash of items are changign
        self.endpoints = UniqList()
        self.drivers = UniqList()
        self._usedOps = {}
        self.negated = False
    
    def simPropagateChanges(self):
        if self._oldVal != self._val or self._oldVal.eventMask != self._val.eventMask:
            conf = self._simulator.config
            env = self._simulator.env
            self._oldVal = self._val
            for e in self.endpoints:
                if conf.log:
                    conf.logger("%d: Signal.simPropagateChanges %s -> %s" % (env.now, self.name, str(e)))
                yield env.process(e.simPropagateChanges())
        
    def staticEval(self):
        # operator writes in self._val new value
        if self.drivers:
            for d in self.drivers:
                d.staticEval()
        else:
                if isinstance(self.defaultVal, Signal):
                        self._val = self.defaultVal._val
                else:
                    if not self._val.vldMask:  # [TODO] find better way how to find out if was initialized
                        self._val = self.defaultVal
        return self._val
    
    def simUpdateVal(self, newVal):
        if not  isinstance(newVal, Value):
            raise SimException("new value is instance of %s it should be instance of value" % (str(newVal.__class__)))
        self._val = newVal
        try:
            env = self._simulator.env
        except AttributeError:
            raise SimNotInitialized("Singal %s does not contains reference to its simulator" % (str(self)))
        c = self._simulator.config
        if  c.log:
            c.logger("%d: %s <= %s" % (env.now, self.name, str(newVal)))
        
        yield env.process(self.simPropagateChanges())
     
    def singleDriver(self):
        if len(self.drivers) != 1:
            raise MultipleDriversExc()
        return list(self.drivers)[0]
            
class SyncSignal(Signal):
    def __init__(self, name, var_type, defaultVal=None):
        super().__init__(name, var_type, defaultVal)
        self.next = Signal(name + "_next", var_type, defaultVal)
        
    def _assignFrom(self, source):
        source = checkOperand(source)
        a = Assignment(source, self.next)
        a.cond = set()
        self.next.drivers.append(a)
        if not isinstance(source, Value):
            source.endpoints.append(a)
             
        return a


def areSameSignals(a, b):
    if a is b:
        return True
    if type(a) != type(b):
        return False 
    if len(a.drivers) != 1 or len(b.drivers) != 1:
        return False
    da = list(a.drivers)[0]
    db = list(b.drivers)[0]
    return da == db
