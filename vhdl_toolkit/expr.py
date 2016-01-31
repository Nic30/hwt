import types
from vhdl_toolkit.synthetisator.param import getParam

def value2vhdlformat(dst, val):
    """ @param dst: is VHDLvariable connected with value """
    if hasattr(val, 'name') and not dst.defaultVal == val:
        return val.name
    w = dst.var_type.getWidth()
    if w == 1:
        return "'%d'" % (int(val))
    elif w == int:
        return "%d" % val.get()
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
        elif operator == BinOp.MINUS:
            evalFn = lambda self : BinOp.getLit(self.op0) - BinOp.getLit(self.op1)
        elif operator == BinOp.DIV:
            evalFn = lambda self : BinOp.getLit(self.op0) // BinOp.getLit(self.op1)
        elif operator == BinOp.MULT:
            evalFn = lambda self : BinOp.getLit(self.op0) * BinOp.getLit(self.op1)
        elif operator == BinOp.DOWNTO:
            evalFn = lambda self : [BinOp.getLit(self.op0), BinOp.getLit(self.op1)]
        else:
            raise Exception("Invalid BinOp operator %s" % (operator))
        self.evalFn = types.MethodType(evalFn, self)
        
    def __call__(self):
        return self.evalFn()
    
    def __str__(self):
        return   ''.join([str(self.op0), " ", self.operator, " ", str(self.op1)])    
