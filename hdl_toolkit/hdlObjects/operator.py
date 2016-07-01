from copy import deepcopy
from hdl_toolkit.synthetisator.rtlLevel.signal import RtlSignal, RtlSignalBase 
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.function import Function

class InvalidOperandExc(Exception):
    pass

class Operator():
    """
    Class of operator in expression tree
    @ivar ops: list of operands
    @ivar evalFn: function to evaluate this operator
    @ivar operator: OpDefinition instance 
    @ivar result: result signal of this operator
    """
    def __init__(self, operator, operands):
        self.ops = list(operands)
        self.operator = operator
        self.result = None
        
    #def simPropagateChanges(self):
    #    """
    #    Called by simulator on input change
    #    """
    #    v = self.evalFn()
    #    try:
    #        sim = self._simulator
    #    except AttributeError:
    #        raise SimNotInitialized("Operator '%s' is not bounded to any simulator" %
    #                                 (str(self)))
    #    env = sim.env
    #    c = sim.config
    #    
    #    yield env.timeout(c.propagDelay(self))
    #    
    #    if c.logPropagation:
    #        # [BUG] str method on Op displays new values, but they are not propageted yet
    #        c.logPropagation('%d: "%s" -> %s' % (env.now, str(self), str(v))) 
    #    yield env.process(self.result.simUpdateVal(v))
    
    def registerSignals(self, outputs=[]):
        """
        Register potential signals to drivers/endpoints
        """
        for o in self.ops:
            if o in outputs:
                o.drivers.append(self)
            elif isinstance(o, RtlSignalBase):
                o.endpoints.append(self)
            elif isinstance(o, (Value, Function)):
                pass
            else:
                raise NotImplementedError("Operator operands can be only signal or values got:%s" % repr(o))
                
    
    def simEval(self):
        """
        Recursively statistically evaluate result of this operator
        if signal has not set hidden flag do not reevaluate it
        """
        for o in self.ops:
            if o.hidden:
                o.simEval()
        self.result._val = self.evalFn()
            
    def staticEval(self):
        """
        Recursively statistically evaluate result of this operator
        """
        for o in self.ops:
            o.staticEval()
        self.result._val = self.evalFn()
            
    def evalFn(self):
        """
        Syntax sugar
        """
        return self.operator.eval(self)
    
    def __eq__(self, other):
        return self is other or (
             type(self) == type(other) 
            and self.operator == other.operator \
            and self.ops == other.ops)
    
    @staticmethod
    def withRes(opDef, operands, resT, outputs=[]):
        """
        Create operator with result signal
        """
        op = Operator(opDef, operands)
        out = RtlSignal(None, resT)
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
