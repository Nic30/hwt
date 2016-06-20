from copy import deepcopy
from hdl_toolkit.simulator.exceptions import SimNotInitialized
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.function import Function

class InvalidOperandExc(Exception):
    pass

class Operator():
    """
    class of operator in expression tree
    @ivar ops: list of operands
    @ivar evalFn: function to evaluate this operator
    @ivar operator: OpDefinition instance 
    @ivar result: result signal of this operator
    """
    def __init__(self, operator, operands):
        self.ops = list(operands)
        self.operator = operator
        self.result = None
        
    def simPropagateChanges(self):
        v = self.evalFn()
        try:
            sim = self._simulator
        except AttributeError:
            raise SimNotInitialized("Operator '%s' is not bounded to any simulator" % (str(self)))
        env = sim.env
        c = sim.config
        
        yield env.timeout(c.opPropagDur)
        
        if c.log:
            # [BUG] str method on Op displays new values, but they are not propageted yet
            c.logger('%d: "%s" -> %s' % (env.now, str(self), str(v))) 
        yield env.process(self.result.simUpdateVal(v))
    
    def registerSignals(self, outputs=[]):
        for o in self.ops:
            if o in outputs:
                o.drivers.append(self)
            elif isinstance(o, Signal):
                o.endpoints.append(self)
            elif isinstance(o, (Value, Function)):
                pass
            else:
                raise NotImplementedError("Operator operands can be only signal or values got:%s" % repr(o))
                
    
    def staticEval(self):
        for o in self.ops:
            o.staticEval()
        self.result._val = self.evalFn()
            
    def evalFn(self):
        return self.operator.eval(self)
    
    def __eq__(self, other):
        return self is other or (
             type(self) == type(other) 
            and self.operator == other.operator \
            and self.ops == other.ops)
    
    @staticmethod
    def withRes(opDef, operands, resT, outputs=[]):
        op = Operator(opDef, operands)
        out = Signal(None, resT)
        out.drivers.append(op)
        out.origin = op
        op.result = out
        op.registerSignals(outputs)
        
        return out
    
    def __deepcopy__(self, memo=None):
        try:
            return memo[self]
        except KeyError:
            o = Operator(None, [])
            memo[id(self)] = o
            for k, v in self.__dict__.items():
                setattr(o, k, deepcopy(v, memo))

            return o
                
    def __hash__(self):
        return hash((self.operator, frozenset(self.ops)))
    
        
    def __repr__(self):
        return "<%s operator:%s, ops:%s>" % (self.__class__.__name__,
                                             repr(self.operator), repr(self.ops))
