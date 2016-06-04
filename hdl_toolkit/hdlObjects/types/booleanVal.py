from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.value import Value

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
        """return abs(w.val[0].val - w.val[1].val) + 1
    
        @attention: ignores eventMask
        """
        self._otherCheck(other)

        eq = self.val == other.val \
            and self.vldMask == other.vldMask == 1
        
        vldMask = int(self.vldMask == other.vldMask == 1)
        evMask = self.eventMask | other.eventMask
        return self.__class__(eq, BOOL, vldMask, eventMask=evMask)

    def __invert__(self):
        v = self.clone()
        v.val = not v.val
        return v

    # logic
    def __and__(self, other):
        self._otherCheck(other)
        # [VHDL-BUG-LIKE] X and 0 should be 0 now is X (in vhdl is now this function correct)
        v = self.val and other.val
        return self.__class__(v, BOOL,
                self.vldMask & other.vldMask,
                self.eventMask | other.eventMask)
        
    def __or__(self, other):
        self._otherCheck(other)
        # [VHDL-BUG-LIKE] X or 1 should be 1 now is X (in vhdl is now this function correct) 
        v = bool(self.val) or bool(other.val)
        return self.__class__(v, BOOL,
                self.vldMask & other.vldMask,
                self.eventMask | other.eventMask)

    def __bool__(self):
        return bool(self.val and self.vldMask)
