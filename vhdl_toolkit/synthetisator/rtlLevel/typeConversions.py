from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
from vhdl_toolkit.hdlObjects.operators import Op

def exprTerm2Bool(e):
    """
    convert terminal from expression to bool expression
    """
    if isinstance(e, int):
        return bool(e)
    elif isinstance(e, Signal):
        return e.opEq(e.onIn)
    else:
        raise TypeError("exprTerm2Bool not implemented for argument of type %s" % 
                         (e.__class__.__name__))

def expr2cond(expr):
    """
    Convert expression to boolean expression
    """
    isBool = returnTypeIsBool(expr)
    if isBool:
        return expr
    else:
        return exprTerm2Bool(expr)
       
def returnTypeIsBool(expr):
    ''' @return: expr, exprIsBoolean '''
    if isinstance(expr, bool):
        return True
    elif isinstance(expr, int):
        return False
    elif isinstance(expr, Signal):
        return expr.var_type.width == bool
    elif isinstance(expr, Op):
        return (expr.getReturnType().width == bool)
    raise Exception('_expr2cond canot convert expr %s' % str(expr))
