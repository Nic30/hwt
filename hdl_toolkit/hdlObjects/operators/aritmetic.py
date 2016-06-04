from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.defs import INT

# [TODO] +,-,*,/   for INT, signed, unsigned



def getReturnType(op):
    t = op.ops[0]._dtype
    if isinstance(t, Integer):
        return INT
    else:
        return t
    
def addOperand(operator, operand):
    t = operand._dtype
    try:
        opType = operator.getReturnType()
    except IndexError:
        opType = t
        
    typeConvertedOp = t.convert(operand, opType)
    operator.ops.append(typeConvertedOp)
    if not isinstance(typeConvertedOp, Value):
        typeConvertedOp.endpoints.add(operator)