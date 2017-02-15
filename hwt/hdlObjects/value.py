    
class Value():
    """
    Wrap around hdl value with overloaded operators
    http://www.rafekettler.com/magicmethods.html
    
    operators are overloaded in every type separately
    """
    __slots__ = ["val", "_dtype", "vldMask", "updateTime"]
    
    def __init__(self, val, _type, vldMask, updateTime=-1):
        self.val = val
        self._dtype = _type
        self.vldMask = vldMask
        self.updateTime = updateTime
    
    def _isFullVld(self):
        return self.vldMask == self._dtype.all_mask()

    def _convert(self, toT):
        return self._dtype.convert(self, toT)

    def staticEval(self):
        return self.clone()
    
    def simEval(self, simulator):
        return self.clone()
    
    def clone(self):
        return self.__class__(self.val, self._dtype, self.vldMask, self.updateTime)
    
    def __hash__(self):
        return hash((self._dtype, self.val, self.vldMask, self.updateTime))
    
    def __repr__(self):
        return "<Value {0:s}, mask {1:b}, time {2:.2f}>".format(
                    str(self.val), self.vldMask, self.updateTime)    

    @classmethod
    def fromPy(cls, val, typeObj):
        raise NotImplementedError("fromPy fn is not implemented for %s" % (str(cls)))
   
    def __nonzero__(self):
        raise NotImplementedError()
    def __bool__(self):
        raise NotImplementedError()
    def __pos__(self):
        raise NotImplementedError()
    def __neg__(self):
        raise NotImplementedError()    
    def __abs__(self):
        raise NotImplementedError()
    def __invert__(self):
        raise NotImplementedError()
    def __round__(self, n):
        raise NotImplementedError()
    def __floor__(self):
        raise NotImplementedError()
    def __ceil__(self):
        raise NotImplementedError()
    def __trunc__(self):
        raise NotImplementedError()
    def __add__(self, other):
        raise NotImplementedError()
    def __sub__(self, other):
        raise NotImplementedError()
    def __mul__(self, other):
        raise NotImplementedError()
    def __floordiv__(self, other):
        raise NotImplementedError()
    def __div__(self, other):
        raise NotImplementedError()
    def __truediv__(self, other):
        raise NotImplementedError()
    def __mod__(self, other):
        raise NotImplementedError()
    def __divmod__(self, other):
        raise NotImplementedError()
    def __pow__(self, other):
        raise NotImplementedError()
    def __lshift__(self, other):
        raise NotImplementedError()
    def __rshift__(self, other):
        raise NotImplementedError()
    def __and__(self, other):
        raise NotImplementedError()
    def __or__(self, other):
        raise NotImplementedError()
    def __xor__(self, other):
        raise NotImplementedError()
    def __eq__(self, other):
        if areValues(self, other):
            return self._dtype == other._dtype and  bool(self._eq(other))
        else:
            super().__eq__(other)
    
    def _eq(self, other):
        raise NotImplementedError()
    def __ne__(self, other):
        eq = self._eq(other)
        eq.val = not eq.val
        return eq
    def _concat(self, other):
        raise NotImplementedError()
    def __lt__(self, other):
        raise NotImplementedError()
    def __le__(self, other):
        raise NotImplementedError()
    def __gt__(self, other):
        raise NotImplementedError()
    def __ge__(self, other):
        raise NotImplementedError()
        
    def _hasEvent(self, now):
        raise NotImplementedError()
    
    def _onRisingEdge(self, now):
        raise NotImplementedError()
    
def areValues(*items):
    res = True
    for i in items:
        res = res and isinstance(i, Value)
    return res
