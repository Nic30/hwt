from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.defs import BOOL


class StringVal(Value):
    
    @classmethod
    def fromPy(cls, val, typeObj):
        assert(isinstance(val, str) or val is None)
        vld = 0 if val is None else 1
        if not vld:
            val = ""
        return cls(val, typeObj, vld)
        
    def _eq(self, other):
        self._otherCheck(other)
        eq = self.val == other.val
        vld = int(self.vldMask and other.vldMask)
        ev = self.eventMask | other.eventMask
        
        return BOOL.getValueCls()(eq, BOOL, vld, eventMask=ev)