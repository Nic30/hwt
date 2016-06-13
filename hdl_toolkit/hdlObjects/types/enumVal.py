from hdl_toolkit.hdlObjects.value import Value, areValues
from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps

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
            valid = True
        assert(isinstance(val, str))
        
        return cls(val, typeObj, valid)
    
    def _eq(self, other):
        """return abs(w.val[0].val - w.val[1].val) + 1
    
        @attention: ignores eventMask
        """
        assert(self._dtype is other._dtype)
        
        if areValues(self, other):
            eq = self.val == other.val \
                and self.vldMask == other.vldMask == 1
            
            vldMask = int(self.vldMask == other.vldMask == 1)
            evMask = self.eventMask | other.eventMask
            return BoolVal(eq, BOOL, vldMask, eventMask=evMask)
        else:
            return Operator.withRes(AllOps.EQ, [self, other], BOOL)
        
    def __ne__(self, other):
        assert(self._dtype is other._dtype)
        
        if areValues(self, other):
            neq = self.val != other.val \
                and self.vldMask == other.vldMask == 1
            
            vldMask = int(self.vldMask == other.vldMask == 1)
            evMask = self.eventMask | other.eventMask
            return BoolVal(neq, BOOL, vldMask, eventMask=evMask)
        else:
            return Operator.withRes(AllOps.NEQ, [self, other], BOOL)
        