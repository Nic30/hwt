from collections import deque
from sympy import Symbol, Or, And, Xor, to_cnf, Not
from sympy.logic.boolalg import simplify_logic
from vhdl_toolkit.hdlObjects.operators import Op
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal

Op2Simpy = {Op.AND_LOG: And,
            Op.OR_LOG: Or,
            Op.NEQ: Xor,
            Op.NOT: Not}
Simpy2Op = {}
for k, v in Op2Simpy.items():
    Simpy2Op[v] = k


class SigSymbol(Symbol):
    __slots__ = Symbol.__slots__ + ["signal"]
    def __new__(cls, signal, **assumptions):
        self = super().__new__(cls, signal.name, **assumptions)
        self.signal = signal
        return self
    
class SpecSymbol(Symbol):
    __slots__ = Symbol.__slots__ + ["data"]
    def __new__(cls, name, data, **assumptions):
        self = super().__new__(cls, name, **assumptions)
        self.data = data
        return self

def toSympyOp(op):
    """ converts expresion to sympy expression """
    if isinstance(op, Signal):
        if hasattr(op, 'origin'):
            return toSympyOp(op.origin)
        else:
            return SigSymbol(op)
    try:
        sop = Op2Simpy[op.operator]
        return sop(map(lambda x : toSympyOp(x), op.op))
    except KeyError:
        pass
    for specialOp in [Op.EVENT, int, Op.RISING_EDGE ]:
        if op.operator == specialOp:
            s = SpecSymbol("ss" + str(id(op)), op)
            return s
    raise Exception("Can not cover token to Sympy token")    

def fromSympyOp(op):
    if isinstance(op, SigSymbol):
        return op.signal
    elif isinstance(op, SpecSymbol):
        return op.data
    else:
        uOpCls = Simpy2Op[op.__class__] 
        uOp = Op(uOpCls, op.args)
        return  uOp
        
    raise Exception("Can not convert symbol '%s' from Sympy" % str(op))
    
def expr_optimize(expr):
    if not expr:
        return expr
    condExpr = list(map(lambda x : toSympyOp(x), expr))  # to CNF of terms in cond
    r = simplify_logic(condExpr)
    return fromSympyOp(r)


class ProcessIfOptimalizer:
    def otimize(self, expr):
        pass
