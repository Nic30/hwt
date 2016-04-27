from hdl_toolkit.hdlObjects.value import Value

class TypeOps():
    @classmethod
    def fromPy(cls, val, typeObj):
        raise NotImplementedError("fromPy fn is not implemented for %s" % (str(cls)))
 

    def mkConversion(self, otherType):
        """
        Generate static or dynamic conversion from this value to value of otherType
        """
        raise NotImplementedError("mkConversion fn is not implemented for %s" % (self.__repr__()))
         
        
    def convert(self, otherType):
        """
        convert this value to value of otherType
        """
        raise NotImplementedError("Type conversion fn is not implemented for %s" % (self.__repr__()))
    
    @classmethod
    def _otherCheck(cls, other):
        assert(isinstance(other, Value))
        assert(issubclass(other.__class__, cls))
        
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
        raise NotImplementedError()
    
    def __ne__(self, other):
        eq = self == other
        eq.val = not eq.val
        return eq
    
    def concat(self, other):
        raise NotImplementedError()
    
    def __lt__(self, other):
        raise NotImplementedError()
        
    def ___le__(self, other):
        raise NotImplementedError()
    
    def __gt__(self, other):
        raise NotImplementedError()
    
    def __ge__(self, other):
        raise NotImplementedError()


