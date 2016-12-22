from hwt.hdlObjects.value import Value, areValues
from hwt.hdlObjects.types.defs import BOOL, INT, SLICE
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.hdlObjects.types.integer import Integer
from operator import pow, add, sub, mul, floordiv, eq, ne, le, lt, ge, gt

BoolVal = BOOL.getValueCls()
SliceVal = SLICE.getValueCls()

def intOp__val(self, other, op, resT, evalFn):
    v = evalFn(self.val, other.val)
    vldMask = int(self.vldMask and other.vldMask)
    updateTime = max(self.updateTime, other.updateTime)
    return resT.getValueCls()(v, resT, vldMask, updateTime)

def intOp(self, other, op, resT, evalFn=None):
    if evalFn is None:
        evalFn = op._evalFn
        
    other = toHVal(other)._convert(INT)
    if areValues(self, other):
        return intOp__val(self, other, op, resT, evalFn)
    else:
        return Operator.withRes(op, [self, other], resT)

def intAritmeticOp(self, other, op):
    return intOp(self, other, op, INT)

def intCmpOp(self, other, op, evalFn=None):
    return intOp(self, other, op, BOOL, evalFn=evalFn)

class IntegerVal(Value):
    """
    @ivar vldMask: can be only 0 or 1
    @ivar updateTime: time when this value was set, used in simulator
    """
    @classmethod
    def fromPy(cls, val, typeObj):
        """
        @param val: value of python type int or None
        @param typeObj: instance of HdlType
        """
        assert isinstance(typeObj, Integer)
        vld = int(val is not None)
        if not vld:
            val = 0
        else:
            val = int(val)
        
        return cls(val, typeObj, vld)
    
    # used only as syntax shugar for simulations
    def __int__(self):
        if self.vldMask:
            return self.val
        else:
            return None
    
    # arithmetic
    def _neg__val(self):
        v = self.clone()
        v.val = -self.val 
        return v
    
    def __neg__(self):
        if isinstance(self, Value):
            return self._neg__val()
        else:
            return Operator.withRes(AllOps.UN_MINUS, [self], INT)

    def _add__val(self, other):
        return intOp__val(self, other, AllOps.ADD, INT, add)
    def __add__(self, other):
        return intAritmeticOp(self, other, AllOps.ADD)
        
    def _sub__val(self, other):
        return intOp__val(self, other, AllOps.SUB, INT, sub)
    def __sub__(self, other):
        return intAritmeticOp(self, other, AllOps.SUB)
    
    def _mul__val(self, other):
        return intOp__val(self, other, AllOps.MUL, INT, mul)
    def __mul__(self, other):
        return intAritmeticOp(self, other, AllOps.MUL)

    def _pow__val(self, other):
        return intOp__val(self, other, AllOps.POW, INT, pow)
    def _pow(self, other):
        return intOp(self, other, AllOps.POW, INT, pow)
    
    def _floordiv__val(self, other):
        return intOp__val(self, other, AllOps.DIV, INT, floordiv)
    def __floordiv__(self, other):
        return intAritmeticOp(self, other, AllOps.DIV)
    
    
    def _downto__val(self, other):
        vldMask = int(self.vldMask and other.vldMask)
        updateTime = max(self.updateTime, other.updateTime)
        return SliceVal((self, other), SLICE, vldMask, updateTime)
    def _downto(self, other):
        other = toHVal(other)._convert(INT)
        if areValues(self, other):
            return self._downto__val(other)
        else:
            return Operator.withRes(AllOps.DOWNTO, [self, other], SLICE)
    
    # comparisons    
    def _eq__val(self, other):
        return intOp__val(self, other, AllOps.EQ, BOOL, eq)
    def _eq(self, other):
        return intCmpOp(self, other, AllOps.EQ, eq)
    
    def _ne__val(self, other):
        return intOp__val(self, other, AllOps.NEQ, BOOL, ne)
    def __ne__(self, other):
        return intCmpOp(self, other, AllOps.NEQ)

    def _le__val(self, other):
        return intOp__val(self, other, AllOps.LE, BOOL, le)
    def __le__(self, other):
        return intCmpOp(self, other, AllOps.LE)
    
    def _lt__val(self, other):
        return intOp__val(self, other, AllOps.LOWERTHAN, BOOL, lt)
    def __lt__(self, other):
        return intCmpOp(self, other, AllOps.LOWERTHAN)
    
    def _ge__val(self, other):
        return intOp__val(self, other, AllOps.GE, BOOL, ge)
    def __ge__(self, other):
        return intCmpOp(self, other, AllOps.GE)
    
    def _gt__val(self, other):
        return intOp__val(self, other, AllOps.GREATERTHAN, BOOL, gt)
