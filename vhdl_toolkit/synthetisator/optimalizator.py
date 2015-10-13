from sympy import Symbol, Or, And, Xor, to_cnf, Not
from vhdl_toolkit.synthetisator.signal import Signal, OpAnd, OpXor, OpNot, OpOr, \
    OpEvent, OpOnRisingEdge, OperatorUnary, OperatorBinary, OpEq
from collections import deque
from sympy.logic.boolalg import simplify_logic


binaryOpTransl = [(OpAnd, And), (OpOr, Or), (OpXor, Xor)  ]
unaryOpTransl = [(OpNot, Not)]

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
    for bOp, sop in binaryOpTransl:
        if isinstance(op, bOp):
            return sop(toSympyOp(op.operand0), toSympyOp(op.operand1))
    for uOp, sop in unaryOpTransl:
        if isinstance(op, uOp):
            return sop(toSympyOp(op.operand))
    for specialOp in [OpEvent, int, OpOnRisingEdge ]:
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
        for uOp, sop in unaryOpTransl:
            if isinstance(op, sop):
                if len(op.args) == 1:
                    return uOp(fromSympyOp(op.args[0]))
                else:
                    raise Exception("Unexpected count of arguments for unary op.")
        for bOp, sop in binaryOpTransl:
            if isinstance(op, sop):
                tb = TreeBalancer(bOp)
                return  tb.balanceExprSet([ fromSympyOp(x) for x in op.args])
        
    raise Exception("Can not convert symbol '%s' from Sympy" % str(op))
    
def expr_optimize(expr):
    if not expr:
        return expr
    tb = TreeBalancer(And)
    condExpr = tb.balanceExprSet(list(map(lambda x : toSympyOp(x), expr)))  # to CNF of terms in cond
    r = simplify_logic(condExpr)
    return fromSympyOp(r)

def exprTerm2Bool(e):
    if hasattr(e, 'onIn'):
        return OpEq(e, e.onIn).result
    else:
        return OpEq(e, 1).result

def expr2cond(expr):
    '''
        Walk down the tree if you discover OpOnRisignEdge convert others on same level to bool by "= 1" then walk up the tree and propagate bool 
        The only difference between expr and cond is that result of cond has to be bool
    '''
    e, isBool = _expr2cond(expr)
    if not isBool:
        return exprTerm2Bool(e)
    else:
        return e

def _expr2cond(expr):
    ''' @return: expr, exprIsBoolean '''
    if isinstance(expr, set):
        isBool = True
        for c in expr:
            e, isB = _expr2cond(c)
            isBool  = isBool and isB
        return expr, isBool
        
        
    elif isinstance(expr, OpOnRisingEdge):
        return expr, True
    elif isinstance(expr, int):
        return expr, False
    elif isinstance(expr, Signal):
        if hasattr(expr, 'origin'):
            return _expr2cond(expr.origin)
        else:
            return expr, False
        
    elif isinstance(expr, OperatorUnary):
        op0, op0_isBool = _expr2cond(expr.operand)
        expr.operand = op0
        return expr, op0_isBool  
         
    elif isinstance(expr, OperatorBinary):
        op0, op0_isBool = _expr2cond(expr.operand0)
        op1, op1_isBool = _expr2cond(expr.operand1)
        if op0_isBool != op1_isBool:
            if op0_isBool:
                expr.operand1 = exprTerm2Bool(op1)
            elif op1_isBool:
                expr.operand0 = exprTerm2Bool(op0)
            return expr, True
        else:
            return expr, op0_isBool
    raise Exception('_expr2cond canot convert expr %s' % str(expr))

class TreeBalancer():
    def __init__(self, operator):
        self.op = operator
        self.root = None
    def balanceExprSet(self, nodes, low=None, high=None):
        """Creates balanced tree with operator and list of nodes"""
        if not nodes:
            return 
        root = nodes[0]
        fifo = deque([nodes[0]])
        nextNode = None
        for n in nodes[1:]:
            tmp = fifo.pop()
            if isinstance(tmp, self.op):
                if isinstance(tmp.operand0, self.op) and isinstance(tmp.operand1, self.op):
                    raise Exception("Cannot extend finished node")
                else:
                    tmp_parent = tmp
                    if not nextNode:  # extend left child
                        tmp = self.op(tmp.operand0, n)
                        tmp_parent.operand0 = tmp.result
                        nextNode = tmp_parent
                        fifo.appendleft(tmp)
                    else:  # extend right child
                        tmp = self.op(tmp.operand1, n)
                        tmp_parent.operand1 = tmp.result
                        fifo.appendleft(tmp)
                        nextNode = None
            else:
                tmp = self.op(tmp, n)
                root = tmp
                fifo.appendleft(tmp)
                
        if hasattr(root, 'result'):
            return root.result
        else:        
            return  root
        
class ProcessIfOptimalizer:
    def otimize(self, expr):
        pass
