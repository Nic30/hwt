from math import log2
import math
from sympy import Symbol, Or, And, Xor, to_cnf, Not
from vhdl_toolkit.synthetisator.signal import Signal, OpAnd, OpXor, OpNot, OpOr, \
    OpEvent, OpOnRisingEdge
from vhdl_toolkit.types import VHDLBoolean
from sympy import sympify
from collections import deque

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

binaryOpTransl = [(OpAnd, And), (OpOr, Or), (OpXor, Xor)  ]
unaryOpTransl = [(OpNot, Not)]

def toSympyOp(op):
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
        
    raise Exception("Can not convert symbol form Sympy")
    
def cond_optimize(cond):
    tb = TreeBalancer(And)
    condExpr = tb.balanceExprSet(list(map(lambda x : toSympyOp(x), cond)))  # to CNF of terms in cond
    r = sympify(condExpr)
    return fromSympyOp(r)

class TreeBalancer():
    
    def __init__(self, operator):
        self.op = operator
        self.root = None
    def balanceExprSet(self, nodes, low=None, high=None):
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
 
        
        
        
        # mid = int(math.floor((low + high) / 2))
        # if high == low:
        #    return expr[mid]
        # else:
        #    if mid == low:
        #        op0 = expr[low]
        #    else :
        #        op0 = self.balanceExprSet(expr, low, mid - 1)
        #        
        #    op1 = self.balanceExprSet(expr, mid + 1, high)
        #        
        #    if op0 is None and op1 is None:
        #        raise Exception("Unexpected")
        #    root = self.op(op0, op1) 
        #    return root
