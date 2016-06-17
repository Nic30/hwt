from hdl_toolkit.hdlObjects.value import Value, areValues
from hdl_toolkit.hdlObjects.types.defs import BOOL, INT, SLICE
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.types.integer import Integer

BoolVal = BOOL.getValueCls()

def intOp(self, other, op, resT, evalFn=None):
    if evalFn is None:
        evalFn = op._evalFn
        
    other = toHVal(other)._convert(INT)
    if areValues(self, other):
        v = evalFn(self.val, other.val)
        vldMask = int(self.vldMask and other.vldMask)
        eventMask = int(self.eventMask or other.eventMask)
        return resT.getValueCls()(v, resT, vldMask, eventMask)
    else:
        return Operator.withRes(op, [self, other], resT)

def intAritmeticOp(self, other, op):
    return intOp(self, other, op, INT)

def intCmpOp(self, other, op, evalFn=None):
    return intOp(self, other, op, BOOL, evalFn=evalFn)

class IntegerVal(Value):
    """
    @ivar vldMask: can be only 0 or 1
    @ivar eventMask: can be only 0 or 1
    """
    @classmethod
    def fromPy(cls, val, typeObj):
        """
        @param val: value of python type int or None
        @param typeObj: instance of HdlType
        """
        assert(isinstance(typeObj, Integer))
        vld = int(val is not None)
        if not vld:
            val = 0
        else:
            val = int(val)
        
        return cls(val, typeObj, vld)
    
    def __int__(self):
        if self.vldMask:
            return self.val
        else:
            return None
    
    # arithmetic
    def __neg__(self):
        if isinstance(self, Value):
            v = self.clone()
            v.val = -self.val 
            return v
        else:
            return Operator.withRes(AllOps.UN_MINUS, [self], INT)
    
    def __add__(self, other):
        return intAritmeticOp(self, other, AllOps.ADD)
        
    def __sub__(self, other):
        return intAritmeticOp(self, other, AllOps.SUB)
    
    def __mul__(self, other):
        return intAritmeticOp(self, other, AllOps.MUL)

    def __floordiv__(self, other):
        return intAritmeticOp(self, other, AllOps.DIV)
    
    
    # comparisons    
    
    def _downto(self, other):
        other = toHVal(other)._convert(INT)
        if areValues(self, other):
            vldMask = int(self.vldMask and other.vldMask)
            eventMask = int(self.eventMask or other.eventMask)
            return SLICE.getValueCls()((self, other), SLICE, vldMask, eventMask)
        else:
            return Operator.withRes(AllOps.DOWNTO, [self, other], SLICE)
    
    def _eq(self, other):
        return intCmpOp(self, other, AllOps.EQ, evalFn=lambda a, b: a == b)
    
    def __ne__(self, other):
        return intCmpOp(self, other, AllOps.NEQ)
    
    def __le__(self, other):
        return intCmpOp(self, other, AllOps.LE)
    def __lt__(self, other):
        return intCmpOp(self, other, AllOps.LOWERTHAN)
    def __ge__(self, other):
        return intCmpOp(self, other, AllOps.GE)
    def __gt__(self, other):
        return intCmpOp(self, other, AllOps.GREATERTHAN)
