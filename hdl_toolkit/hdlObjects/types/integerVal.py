from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.defs import BOOL, INT

BoolVal = BOOL.getValueCls()

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
        
    def _eq(self, other):
        self._otherCheck(other)
        vld = self.vldMask and other.vldMask
        eq = self.val == other.val and vld
        ev = self.eventMask or other.eventMask
        
        return BoolVal(eq, BOOL, vld, eventMask=ev)
    
    def __neg__(self):
        v = self.clone()
        v.val = -self.val 
        return v
    
    def __add__(self, other):
        self._otherCheck(other)
        v = self.val + other.val
        vldMask = int(self.vldMask and other.vldMask)
        eventMask = int(self.eventMask or other.eventMask)

        return self.__class__(v, INT, vldMask, eventMask)
        
    def __sub__(self, other):
        return self +(-other)
    
    def __mul__(self, other):
        self._otherCheck(other)
        val = self.val * other.val
        vldMask = int(self.vldMask and other.vldMask)
        eventMask = int(self.eventMask or other.eventMask)
        
        return self.__class__(val, INT, vldMask, eventMask=eventMask)
    
    def __floordiv__(self, other):
        self._otherCheck(other)
        val = self.val // other.val
        vldMask = int(self.vldMask and other.vldMask)
        eventMask = int(self.eventMask or other.eventMask)

        return self.__class__(val, INT, vldMask, eventMask=eventMask)
    
    def __lt__(self, other):
        self._otherCheck(other)  
        val = self.val < other.val
        vldMask = int(self.vldMask and other.vldMask)
        eventMask = int(self.eventMask or other.eventMask)
        
        return BoolVal(val, BOOL, vldMask, eventMask=eventMask)

    def __gt__(self, other):
        self._otherCheck(other)  
        val = self.val > other.val
        vldMask = int(self.vldMask and other.vldMask)
        eventMask = int(self.eventMask or other.eventMask)
        
        return BoolVal(val, BOOL, vldMask, eventMask=eventMask)
