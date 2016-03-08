from vhdl_toolkit.simExceptions import SimNotInitialized

class InvalidOperandExc(Exception):
    pass

class Op():
    """
    class of operator in expression tree
    @ivar ops: list of operands
    @ivar evalFn: function to evaluate this operator
    @ivar operator: OpDefinition instance 
    @ivar result: result signal of this operator
    """
    def __init__(self, operator, operands):
        self.ops = list()
        for op in operands:
            operator.addOperand(self, op)
        self.evalFn = lambda : self.operator.eval(self)
        self.operator = operator
        
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
        
    def getReturnType(self):
        return self.operator.getReturnType(self)
    
    def __str__(self):
        return self.operator.str(self)
