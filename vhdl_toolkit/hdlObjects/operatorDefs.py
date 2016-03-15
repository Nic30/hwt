from vhdl_toolkit.hdlObjects.typeDefs import BOOL, INT, RANGE
from vhdl_toolkit.hdlObjects.value import Value

def convOpsToType(t):
        def addOperand(operator, operand):
            opAsBool = operand.dtype.convert(operand, t)
            if not isinstance(opAsBool, Value):
                opAsBool.endpoints.add(operator)
            operator.ops.append(opAsBool)
        return addOperand

addOperand_logic = convOpsToType(BOOL)    


class OpDefinition():
    @staticmethod
    def addOperand_default(operator, operand):
        t = operand.dtype
        try:
            opType = operator.getReturnType()
        except IndexError:
            opType = t
            
        typeConvertedOp = t.convert(operand, opType)
        operator.ops.append(typeConvertedOp)
        if not isinstance(typeConvertedOp, Value):
            typeConvertedOp.endpoints.add(operator)
        

    
    @staticmethod
    def addOperand_eq(operator, operand):
        t = operand.dtype
        try:
            opType = OpDefinition.getReturnType_default(operator)
        except IndexError:
            opType = t
            
        typeConvertedOp = t.convert(operand, opType)
        operator.ops.append(typeConvertedOp)
        if not isinstance(typeConvertedOp, Value):
            typeConvertedOp.endpoints.add(operator)
    
       
    @staticmethod
    def getReturnType_default(op):
        return op.ops[0].dtype

    def __init__(self, _id, precedence, strOperatorOrFn, evalFn,
                 getReturnType=getReturnType_default.__func__ ,
                 addOperand=addOperand_default.__func__):  
        # (addOperand_default is staticmethod object)
        self.id = _id
        self.precedence = precedence
        self.strOperator = strOperatorOrFn
        self._evalFn = evalFn
        self.getReturnType = getReturnType
        self.addOperand = addOperand
    
    def eval(self, operator):
        """Load all operands and process them by self._evalFn"""
        it = iter(operator.ops)

        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('OpDefinition.eval, can not reduce empty sequence ')
        
        argc = self._evalFn.__code__.co_argcount
        if argc == 1:
            return self._evalFn(initializer)
        elif argc == 2:
            accum_value = initializer
            for x in it:
                accum_value = self._evalFn(accum_value, x)
            return accum_value
        else:
            raise NotImplementedError()
        
    def str(self, operator, serializer):
        from vhdl_toolkit.hdlObjects.operators import Operator
        
        def p(op):
            s = serializer.Value(op)
            if isinstance(op, Operator) and op.operator.precedence > self.precedence:
                return " (%s) " % s
            return " %s " % s
             
        if isinstance(self.strOperator, str):
            return  self.strOperator.join(map(p, operator.ops))
        else:
            return self.strOperator(list(map(p, operator.ops)))
        
    def __repr__(self):
        return "<OpDefinition %s>" % (self.strOperator)
            
class AllOps():
    """
    https://en.wikipedia.org/wiki/Order_of_operations
    @attention: Remember that and operator is & and or is |, 'and' and 'or' can not be used because
    they can not be overloaded
    @attention: These are internal operators, the are not equal to verilog or vhdl operators
    """
    
    NOT = OpDefinition('NOT', 3, lambda op: "NOT " + str(op[0]),  # [TODO] [0] has dangerous potential
                       lambda a :~a, lambda op: BOOL,
                       addOperand=addOperand_logic)
    EVENT = OpDefinition('EVENT', 3, lambda op:  str(op) + "'EVENT",
                         lambda a : NotImplemented(),
                         lambda op: BOOL)
    RISING_EDGE = OpDefinition('RISING_EDGE', 3, lambda op: "RISING_EDGE(" + str(op) + ")",
                       lambda a : NotImplemented())
    DIV = OpDefinition('DIV', 3, '/', lambda a, b : a // b)
    PLUS = OpDefinition('PLUS', 4, '+', lambda a, b : a + b)
    MINUS = OpDefinition('MINUS', 4, '-', lambda a, b : a - b)
    MULT = OpDefinition('MULT', 4, '*', lambda a, b : a * b)
    NEQ = OpDefinition('NEQ', 7, '!=', lambda a, b : a != b,
                        lambda op: BOOL)
    XOR = OpDefinition('XOR', 7, 'XOR', lambda a, b : a != b,
                        lambda op: BOOL,
                       addOperand=addOperand_logic)
    EQ = OpDefinition('EQ', 7, '==', lambda a, b : a == b,
                        lambda op: BOOL,
                        addOperand=OpDefinition.addOperand_eq)
    AND_LOG = OpDefinition('AND', 11, 'AND', lambda a, b : a & b,
                        lambda op: BOOL,
                       addOperand=addOperand_logic)
    OR_LOG = OpDefinition('OR', 12, 'OR', lambda a, b : a | b,
                        lambda op: BOOL,
                       addOperand=addOperand_logic)
    DOWNTO = OpDefinition("DOWNTO", 13, 'DOWNTO',
                        lambda a, b : Value.fromPyVal([b, a], RANGE),  # [TODO]
                        lambda op: RANGE,
                        addOperand=convOpsToType(INT))
    allOps = {}
    for op in [PLUS, MINUS, DIV, MULT, DOWNTO]:
        assert (op.id not in allOps)
        allOps[op.id] = op
        
    @classmethod
    def opByName(cls, name):
        return cls.allOps[name]
