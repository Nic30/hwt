from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.value import Value, areValues
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.types.typeCast import toHVal

def boolLogOp(self, other, op):
    other = toHVal(other)

    if areValues(self, other):
        v = bool(op._evalFn(bool(self.val), (other.val)))
        return BooleanVal(v, BOOL,
                self.vldMask & other.vldMask,
                max(self.updateTime,  other.updateTime))
    else:
        return Operator.withRes(op, [self, other._convert(BOOL)], BOOL)

def boolCmpOp(self, other, op, evalFn=None):
    other = toHVal(other)
    if evalFn is None:
        evalFn = op._evalFn
    
    if areValues(self, other):
        v = evalFn(bool(self.val), bool(other.val)) and (self.vldMask == other.vldMask == 1)
        return BooleanVal(v, BOOL,
                self.vldMask & other.vldMask,
                max(self.updateTime,  other.updateTime))
    else:
        return Operator.withRes(op, [self, other._convert(BOOL)], BOOL)

class BooleanVal(Value):
    
    @classmethod
    def fromPy(cls, val, typeObj):
        """
        @param val: value of python type bool or None
        @param typeObj: instance of HdlType
        """
        vld = int(val is not None)
        if not vld:
            val = False
        else:
            val = bool(val)
        return cls(val, typeObj, vld)
            
    def _eq(self, other):
        return boolCmpOp(self, other, AllOps.EQ, evalFn=lambda a, b: a == b)

    def __ne__(self, other):
        return boolCmpOp(self, other, AllOps.NEQ)

    def __invert__(self):
        if isinstance(self, Value):
            v = self.clone()
            v.val = not v.val
            return v
        else:
            return Operator.withRes(AllOps.NOT, [self], BOOL)

    def _ternary(self, ifTrue, ifFalse):
        ifTrue = toHVal(ifTrue)
        ifFalse = toHVal(ifFalse)
        
        if isinstance(self, Value):
            if self.val:
                return ifTrue
            else:
                return ifFalse
        else:
            return Operator.withRes(AllOps.TERNARY, [self, ifTrue, ifFalse], ifTrue._dtype)

    def _hasEvent(self, now):
        if isinstance(self, Value):
            return BooleanVal(self.updateTime == now, BOOL, self.vldMask, now)
        else:
            return Operator.withRes(AllOps.EVENT, [self], BOOL)
    


    # logic
    def __and__(self, other):
        # [VHDL-BUG-LIKE] X and 0 should be 0 now is X (in vhdl is now this function correct)
        return boolLogOp(self, other, AllOps.AND_LOG)
        
    def __or__(self, other):
        # [VHDL-BUG-LIKE] X or 1 should be 1 now is X (in vhdl is now this function correct) 
        return boolLogOp(self, other, AllOps.OR_LOG)

    # for evaluating only, not convertible to hdl
    
    def __bool__(self):
        assert isinstance(self, Value)
        return bool(self.val and self.vldMask)
    
