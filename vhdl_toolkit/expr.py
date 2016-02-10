import types
from vhdl_toolkit.synthetisator.param import getParam
import math

class Unconstrained():
    __slots__ = ["derivedWidth"]

def value2vhdlformat(dst, val):
    """ @param dst: is VHDLvariable connected with value """
    if hasattr(val, 'name') and not dst.defaultVal == val:
        return val.name
    w = dst.var_type.getWidth()
    if w == 1:
        return "'%d'" % (int(getParam(val)))
    elif w == int:
        return "%d" % getParam(val.get())
    elif w == Unconstrained:
        v = getParam(val)
        if hasattr(w, "derivedWidth"):
            bits = w.derivedWidth
        else:
            bits = v.bit_length() 
        return ('X"%0' + str(math.ceil(bits / 4)) + 'x"') % (getParam(val))
    elif w == str:
        return '"%s"' % (getParam(val))
    elif w == bool:
        return '%s' % (str(bool(getParam(val))))
    elif w > 1:
        return "STD_LOGIC_VECTOR(TO_UNSIGNED(%d, %s'LENGTH))" % (int(val), dst.name)
    else:
        raise Exception("value2vhdlformat can not resolve type conversion") 

class Map():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def __str__(self):
        return "%s => %s" % (self.dst.name, self.src.name)  
        
   
class Assignment():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        
    def __str__(self):
        return "%s <= %s" % (self.dst.name, value2vhdlformat(self.dst, self.src))

class Literal():
    def __init__(self, _id=None, val=None):
        self.id = _id
        self.val = val
        assert(bool(id) != bool(val))
        if id:
            self.eval = lambda self : id.get()
        else:
            self.eval = lambda self : self.val

class BinOp():
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    DIV = 'DIV'
    MULT = 'MULT'
    DOWNTO = "DOWNTO"
    
    @staticmethod
    def getLit(lit):
        if hasattr(lit, "__call__"):  # is param
            return BinOp.getLit(lit())
        else:
            return getParam(lit)
        
    def __init__(self, op0, operator, op1):
        self.op0 = op0
        self.operator = operator
        
        self.op1 = op1
        
        if operator == BinOp.PLUS:
            evalFn = lambda self : BinOp.getLit(self.op0) + BinOp.getLit(self.op1)
            strOperator = '+'
        elif operator == BinOp.MINUS:
            evalFn = lambda self : BinOp.getLit(self.op0) - BinOp.getLit(self.op1)
            strOperator = '-'
        elif operator == BinOp.DIV:
            evalFn = lambda self : BinOp.getLit(self.op0) // BinOp.getLit(self.op1)
            strOperator = '/'
        elif operator == BinOp.MULT:
            evalFn = lambda self : BinOp.getLit(self.op0) * BinOp.getLit(self.op1)
            strOperator = '*'
        elif operator == BinOp.DOWNTO:
            evalFn = lambda self : [BinOp.getLit(self.op0), BinOp.getLit(self.op1)]
            strOperator = 'DOWNTO'
        else:
            raise NotImplementedError("Unimplemented BinOp operator %s" % (operator))
        self.evalFn = types.MethodType(evalFn, self)
        self.strOperator = strOperator
    def __call__(self):
        return self.evalFn()
    
    def __str__(self):
        return  ''.join([str(self.op0), " ", self.strOperator, " ", str(self.op1)])    
