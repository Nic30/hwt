from hdl_toolkit.hdlObjects.typeDefs import UINT, PINT, INT
from hdl_toolkit.hdlObjects.value import Value

# [TODO] +,-,*,/   for INT, signed, unsigned



def getReturnType(op):
    t = op.ops[0].dtype
    if(t == UINT or t == PINT):
        return INT
    else:
        return t
    
def addOperand(operator, operand):
    t = operand.dtype
    try:
        opType = operator.getReturnType()
    except IndexError:
        opType = t
        
    typeConvertedOp = t.convert(operand, opType)
    operator.ops.append(typeConvertedOp)
    if not isinstance(typeConvertedOp, Value):
        typeConvertedOp.endpoints.add(operator)