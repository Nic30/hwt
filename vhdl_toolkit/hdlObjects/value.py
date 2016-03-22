    
class Value():
    """
    Wrap around hdl value with overloaded operators
    http://www.rafekettler.com/magicmethods.html
    
    """
    def __init__(self, val, _type, vldMask, eventMask=0):
        if isinstance(val, Value):
            val = val.val
        
        assert(val is None or isinstance(val, int) 
               or isinstance(val, bool) 
               or isinstance(val, str) 
               or isinstance(val, float) 
               or isinstance(val, Value) 
               or isinstance(val, list))
        self.val = val
        self.dtype = _type
        self.vldMask = vldMask
        self.eventMask = eventMask
    
   
    @classmethod
    def fromPyVal(cls, val, _type):
        """
        @param val: normal python value
        @param _type: instance of HdlType
        """
        c = _type.ValueCls
        if isinstance(val, c):
            assert(val.dtype.convert(val, _type))
            return val
        self = c.fromPy(val, _type)
        return self
    def staticEval(self):
        return self
    
    def clone(self):
        return self.__class__(self.val, self.dtype, self.vldMask, eventMask=self.eventMask)
    
    def __hash__(self):
        return hash((self.dtype, self.val, self.vldMask, self.eventMask))
    
    def __repr__(self):
        return "<Value {0:s}, vldMask {1:b}, eventMask {2:b}>".format(
                    str(self.val), self.vldMask, self.eventMask)    
