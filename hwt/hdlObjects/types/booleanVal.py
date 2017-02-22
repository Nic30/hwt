from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.types.defs import BOOL
from hwt.hdlObjects.types.eventCapableVal import EventCapableVal
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.hdlObjects.value import Value, areValues
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.hdlObjects.types.bitVal_bitOpsVldMask import vldMaskForOr, \
    vldMaskForAnd
from operator import eq, ne

def boolLogOp__val(self, other, op, getVldFn):
    v = bool(op._evalFn(bool(self.val), (other.val)))
    return BooleanVal(v, BOOL,
            getVldFn(self, other),
            max(self.updateTime, other.updateTime))

def boolLogOp(self, other, op, getVldFn, whenOneIsVal):
    other = toHVal(other)

    if isinstance(self, Value):
        if isinstance(other, Value):
            return boolLogOp__val(self, other, op, getVldFn)

        return whenOneIsVal(self, other)
    else:
        if isinstance(other, Value):
            return whenOneIsVal(other, self)
        
    return Operator.withRes(op, [self, other._convert(BOOL)], BOOL)

def boolCmpOp__val(self, other, op, evalFn):
    v = evalFn(bool(self.val), bool(other.val)) and (self.vldMask == other.vldMask == 1)
    return BooleanVal(v, BOOL,
            self.vldMask & other.vldMask,
            max(self.updateTime, other.updateTime))
    
def boolCmpOp(self, other, op, evalFn=None):
    other = toHVal(other)
    if evalFn is None:
        evalFn = op._evalFn
    
    if areValues(self, other):
        return boolCmpOp__val(self, other, op, evalFn)
    else:
        return Operator.withRes(op, [self, other._convert(BOOL)], BOOL)

def whenOneIsVal_and(val, other):
    if val.vldMask:
        if val.val:
            return other
        else:
            v = val.clone()
            v.val = 0
            return v
    else:
        return val
    

def whenOneIsVal_or(val, other):
    if val.vldMask:
        if val.val:
            return val
        else:
            return other
    else:
        return val
    
class BooleanVal(EventCapableVal):
    
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

    def _eq__val(self, other):
        return boolCmpOp__val(self, other, AllOps.EQ, eq)
    def _eq(self, other):
        return boolCmpOp(self, other, AllOps.EQ, evalFn=eq)

    def _ne__val(self, other):
        return boolCmpOp__val(self, other, AllOps.NEQ, ne)
    def __ne__(self, other):
        return boolCmpOp(self, other, AllOps.NEQ)

    def _invert__val(self):
        v = self.clone()
        v.val = not v.val
        return v
    def __invert__(self):
        if isinstance(self, Value):
            return self._invert__val()
        else:
            try:
                # double negation
                d = self.singleDriver()
                if isinstance(d, Operator) and d.operator == AllOps.NOT:
                    return d.ops[0]
            except MultipleDriversExc:
                pass
            return Operator.withRes(AllOps.NOT, [self], BOOL)

    def _ternary__val(self, ifTrue, ifFalse):
        if self.val:
            if not self.vldMask:
                ifTrue.vldMask = 0
            return ifTrue
        else:
            if not self.vldMask:
                ifFalse.vldMask = 0
            return ifFalse
    def _ternary(self, ifTrue, ifFalse):
        ifTrue = toHVal(ifTrue)
        ifFalse = toHVal(ifFalse)
        
        if isinstance(self, Value):
            return self._ternary__val(ifTrue, ifFalse)
        else:
            return Operator.withRes(AllOps.TERNARY, [self, ifTrue, ifFalse], ifTrue._dtype)

    # logic
    def _and__val(self, other):
        return boolLogOp__val(self, other, AllOps.AND_LOG, vldMaskForAnd)
    def __and__(self, other):
        return boolLogOp(self, other, AllOps.AND_LOG, vldMaskForAnd, whenOneIsVal_and)

    def _or__val(self, other):
        return boolLogOp__val(self, other, AllOps.OR_LOG, vldMaskForOr)
    def __or__(self, other):
        return boolLogOp(self, other, AllOps.OR_LOG, vldMaskForOr, whenOneIsVal_or)


    # for evaluating only, not convertible to hdl
    def __bool__(self):
        assert isinstance(self, Value)
        return bool(self.val and self.vldMask)
    
