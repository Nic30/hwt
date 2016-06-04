from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.defs import BOOL


class ArrayVal(Value):
    
    @classmethod
    def fromPy(cls, val, typeObj):
        if val is None:
            val = [None for _ in range(typeObj.size)]
        assert(len(val) == typeObj.size)
        elements = []
        for v in val:
            if hasattr(v, "name"):  # is signal
                assert(v._dtype == typeObj.elmType)
                e = v
            else:   
                e = typeObj.elmType.fromPy(v)
            elements.append(e)
        
        
        return cls(elements, typeObj, 1)
    
    def _eq(self, other):
        assert(self._dtype.elmType == other._dtype.elmType)
        assert(self._dtype.size == other._dtype.size)
        
        eq = True
        first = self.val[0]
        vld = first.vldMask
        ev = first.eventMask
        
        for a, b in zip(self.val, other.val):
            eq = eq and a == b
            vld = vld & a.vldMask & b.vldMask
            ev = ev & a.eventMask & b.eventMask
        return BOOL.getValueCls()(eq, BOOL, vld, eventMask=ev)
