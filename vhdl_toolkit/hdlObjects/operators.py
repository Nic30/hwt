import types
from vhdl_toolkit.hdlObjects.typeDefinitions import VHDLBoolean


class OpDefinition():
    
    @staticmethod
    def addOperand_default(operator, operand):
        operator.op.append(operand)
    
    @staticmethod
    def addOperand_logic(operator, operand):
        from vhdl_toolkit.synthetisator.rtlLevel.typeConversions import expr2cond
        operator.op.append(expr2cond(operand))
    
    def __init__(self, _id, precedence, strOperatorOrFn, evalFn,
                 getReturnType=lambda op : op.op[0].var_type,
                 addOperand=addOperand_default.__func__): # (addOperand_default is staticmethod object)
        self.id = _id
        self.precedence = precedence
        self.strOperator = strOperatorOrFn
        self._evalFn = evalFn
        self.getReturnType = getReturnType
        self.addOperand = addOperand
    
    def eval(self, operator):
        it = iter(operator.op)
        try:
            initializer = Op.getLit(next(it))
        except StopIteration:
            raise TypeError('OpDefinition.eval, can not reduce empty sequence ')
        accum_value = initializer
        for x in it:
            accum_value = self._evalFn(accum_value, Op.getLit(x))
        return accum_value
    
    def str(self, op):
        def p(op):
            if isinstance(op, Op) and op.operator.precedence > self.precedence:
                return "(%s)" % str(op)
            else:
                return str(op)
             
        if isinstance(self.strOperator, str):
            return  self.strOperator.join(map(p, self.op))
        else:
            return self.strOperator(map(p, op))
    def __repr__(self):
        return "<OpDefinition %s>" % (self.strOperator)
            
class AllOps():
    # https://en.wikipedia.org/wiki/Order_of_operations
    NOT = OpDefinition('NOT', 3, lambda op: "NOT " + str(op),
                       lambda a : not a, lambda op: VHDLBoolean(),
                       OpDefinition.addOperand_logic)
    EVENT = OpDefinition('EVENT', 3, lambda op:  str(op) + "'EVENT", 
                         lambda a : NotImplemented(),
                         lambda op: VHDLBoolean())
    RISING_EDGE = OpDefinition('RISING_EDGE', 3, lambda op: "RISING_EDGE(" + str(op) + ")",
                       lambda a : NotImplemented())
    DIV = OpDefinition('DIV', 3, '/', lambda a, b : a // b)
    PLUS = OpDefinition('PLUS', 4, '+', lambda a, b : a + b)
    MINUS = OpDefinition('MINUS', 4, '-', lambda a, b : a - b)
    MULT = OpDefinition('MULT', 4, '*', lambda a, b : a * b)
    NEQ = OpDefinition('NEQ', 7, '!=', lambda a, b : a != b,
                        lambda op: VHDLBoolean())
    XOR = OpDefinition('XOR', 7, 'XOR', lambda a, b : a != b,
                        lambda op: VHDLBoolean(),
                       OpDefinition.addOperand_logic)
    EQ = OpDefinition('EQ', 7, '==', lambda a, b : a == b,
                        lambda op: VHDLBoolean())
    AND_LOG = OpDefinition('AND', 11, 'AND', lambda a, b : a and b,
                        lambda op: VHDLBoolean(),
                       OpDefinition.addOperand_logic)
    OR_LOG = OpDefinition('OR', 12, 'OR', lambda a, b : a or b,
                        lambda op: VHDLBoolean(),
                       OpDefinition.addOperand_logic)
    DOWNTO = OpDefinition("DOWNTO", 13, 'DOWNTO', lambda a, b : [a, b],
                        lambda op: list)
    allOps = {}
    for op in [PLUS, MINUS, DIV, MULT, DOWNTO]:
        assert (op.id not in allOps)
        allOps[op.id] = op
        
    @classmethod
    def opByName(cls, name):
        return cls.allOps[name]
        
class Op(AllOps):

    def __init__(self, operator, operands):
        self.op = list()
        for op in operands:
            operator.addOperand(self, op)
        self.__call__ = types.MethodType(lambda self : self.operator.eval(self), self)
        self.operator = operator
        
    def __call__(self):
        return self.evalFn()
    
    def getReturnType(self):
        return self.operator.getReturnType(self)
    
    def __str__(self):
        return self.operator.str(self)
