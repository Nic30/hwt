from hwt.hdlObjects.value import Value, areValues
from hwt.hdlObjects.types.defs import BOOL
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps

BoolVal = BOOL.getValueCls()

class EnumVal(Value):
    @classmethod
    def fromPy(cls, val, typeObj):
        """
        @param val: value of python type bool or None
        @param typeObj: instance of HdlType
        """
        if val is None:
            valid = False
            val = typeObj._allValues[0]
        else:
            assert isinstance(val, str)
            valid = True
        
        return cls(val, typeObj, valid)
    
    def _eq__val(self, other):
        eq = self.val == other.val \
             and self.vldMask == other.vldMask == 1
        
        vldMask = int(self.vldMask == other.vldMask == 1)
        updateTime = max(self.updateTime, other.updateTime)
        return BoolVal(eq, BOOL, vldMask, updateTime)
    def _eq(self, other):
        assert self._dtype is other._dtype
        
        if areValues(self, other):
            return self._eq__val(other)
        else:
            return Operator.withRes(AllOps.EQ, [self, other], BOOL)
    
    
    def _ne__val(self, other):
        neq = self.val != other.val \
            and self.vldMask == other.vldMask == 1
        
        vldMask = int(self.vldMask == other.vldMask == 1)
        updateTime = max(self.updateTime, other.updateTime)
        return BoolVal(neq, BOOL, vldMask, updateTime)   
     
    def __ne__(self, other):
        assert self._dtype is other._dtype
        
        if areValues(self, other):
            return self._ne__val(other)
        else:
            return Operator.withRes(AllOps.NEQ, [self, other], BOOL)
        
