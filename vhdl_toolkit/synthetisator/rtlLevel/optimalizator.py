from collections import deque
from sympy import Symbol, Or, And, Xor, to_cnf, Not
from sympy.logic.boolalg import simplify_logic
from vhdl_toolkit.hdlObjects.operators import Op
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal, SignalNode

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
        if isinstance(op, specialOp):
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
    #tb = TreeBalancer(And)
    #tb.balanceExprSet()
    condExpr = list(map(lambda x : toSympyOp(x), expr))  # to CNF of terms in cond
    r = simplify_logic(condExpr)
    return fromSympyOp(r)


#class TreeBalancer():
#    def __init__(self, operator):
#        self.op = operator
#        self.root = None
#        
#    def balanceExprSet(self, nodes, low=None, high=None):
#        """Creates balanced tree with operator and list of nodes"""
#        def isOperator(operand, operator):
#            return isinstance(operand, Op) and operand.operator == operator
#                 
#        if not nodes:
#            return 
#        root = nodes[0]
#        fifo = deque([nodes[0]])
#        nextNode = None
#        for n in nodes[1:]:
#            tmp = fifo.pop()
#            if isOperator(tmp, self.op):
#                if isOperator(tmp.op[0], self.op) and isOperator(tmp.op[1], self.op):
#                    raise Exception("Cannot extend finished node")
#                else:
#                    tmp_parent = tmp
#                    if not nextNode:  # extend left child
#                        tmp = SignalNode.resForOp(Op(self.op, [tmp.op[0], n]))
#                        tmp_parent.op[0] = tmp.result
#                        nextNode = tmp_parent
#                        fifo.appendleft(tmp)
#                    else:  # extend right child
#                        tmp = SignalNode.resForOp(Op(self.op, [tmp.op[1], n]))
#                        tmp_parent.op[1] = tmp.result
#                        fifo.appendleft(tmp)
#                        nextNode = None
#            else:
#                tmp = SignalNode.resForOp(Op(self.op, [tmp, n]))
#                root = tmp
#                fifo.appendleft(tmp)
#                
#        if isinstance(root, Op):
#            return root.result
#        else:        
#            return  root
        
class ProcessIfOptimalizer:
    def otimize(self, expr):
        pass
