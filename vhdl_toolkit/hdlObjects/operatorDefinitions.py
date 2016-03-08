from vhdl_toolkit.hdlObjects.literal import Literal
from vhdl_toolkit.hdlObjects.typeDefinitions import VHDLBoolean
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlContext import mkType
from vhdl_toolkit.synthetisator.param import getParam


class OpDefinition():
    
    @staticmethod
    def addOperand_default(operator, operand):
        operator.ops.append(operand)
        if not isinstance(operand, Value):
            operand.endpoints.add(operator)
        
    
    @staticmethod
    def addOperand_logic(operator, operand):
        if isinstance(operand, Value):
            opAsBool = Value.convertVal(operand, bool)
        else:  # is signal
            if operand.var_type.width == bool:
                opAsBool = operand
            else:
                opAsBool = operand.opEq(operand.onIn)
        if not isinstance(opAsBool, Value):
            opAsBool.endpoints.add(operator)
        operator.ops.append(opAsBool)
        
    @staticmethod
    def getReturnType_default(op):
        try:
            return op.ops[0].var_type
        except AttributeError:
            w = getParam(op.ops[0]).widthOrType
            return mkType(None, w)

    def __init__(self, _id, precedence, strOperatorOrFn, evalFn,
                 getReturnType=getReturnType_default.__func__ ,
                 addOperand=addOperand_default.__func__):  # (addOperand_default is staticmethod object)
        self.id = _id
        self.precedence = precedence
        self.strOperator = strOperatorOrFn
        self._evalFn = evalFn
        self.getReturnType = getReturnType
        self.addOperand = addOperand
    
    def eval(self, operator):
        """Load all operands and process them by self._evalFn"""
        def getVal(o):
            """Load operand"""
            l = Literal.get(o)
            try:
                return l._val
            except AttributeError:
                return l

        it = iter(operator.ops)

        try:
            initializer = getVal(next(it))
        except StopIteration:
            raise TypeError('OpDefinition.eval, can not reduce empty sequence ')
        
        argc = self._evalFn.__code__.co_argcount
        if argc == 1:
            return self._evalFn(initializer)
        elif argc == 2:
            accum_value = initializer
            for x in it:
                accum_value = self._evalFn(accum_value, getVal(x))
            return accum_value
        else:
            raise NotImplementedError()
        
    def str(self, op):
        from vhdl_toolkit.hdlObjects.operators import Op
        
        def p(op):
            if isinstance(op, Op) and op.operator.precedence > self.precedence:
                return " (%s) " % str(op)
            elif isinstance(op, Value):
                return " " + op.asVhdl() + " "
            else:
                return " " + str(op) + " "
             
        if isinstance(self.strOperator, str):
            return  self.strOperator.join(map(p, op.ops))
        else:
            return self.strOperator(list(map(p, op.ops)))
        
    def __repr__(self):
        return "<OpDefinition %s>" % (self.strOperator)
            
class AllOps():
    """
    https://en.wikipedia.org/wiki/Order_of_operations
    @attention: Remember that and operator is & and or is |, 'and' and 'or' can not be used because
    they can not be overloaded
    """
    
    NOT = OpDefinition('NOT', 3, lambda op: "NOT " + str(op[0]),  # [TODO] [0] has dangerous potential
                       lambda a :-a, lambda op: VHDLBoolean(),
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
    AND_LOG = OpDefinition('AND', 11, 'AND', lambda a, b : a & b,
                        lambda op: VHDLBoolean(),
                       OpDefinition.addOperand_logic)
    OR_LOG = OpDefinition('OR', 12, 'OR', lambda a, b : a | b,
                        lambda op: VHDLBoolean(),
                       OpDefinition.addOperand_logic)
    DOWNTO = OpDefinition("DOWNTO", 13, 'DOWNTO', lambda a, b : [a, b],
                        lambda op: mkType(None, list))
    allOps = {}
    for op in [PLUS, MINUS, DIV, MULT, DOWNTO]:
        assert (op.id not in allOps)
        allOps[op.id] = op
        
    @classmethod
    def opByName(cls, name):
        return cls.allOps[name]
