    
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
    def getValClass(cls, _type):
        # _type has to be instance or class derived from HdlType
        if _type.valueCls:
            c = _type.valueCls
        else:
            # dynamically create value class for _type 
            c = type("%s_val" % _type.__class__.__name__, (cls, _type.Ops,), {})
            _type.valueCls = c
        return c
    
    @classmethod
    def fromPyVal(cls, val, _type):
        """
        @param val: normal python value
        @param _type: instance of HdlType
        """
        c = cls.getValClass(_type)
        if isinstance(val, c):
            assert(val.dtype == _type)
            return val
        self = c.fromPy(val, _type)
        return self
    
    def clone(self):
        return self.__class__(self.val, self.dtype, self.vldMask, eventMask=self.eventMask)
    
    def __repr__(self):
        return "<Value {0:s}, vldMask {1:b}, eventMask {2:b}>".format(
                    str(self.val), self.vldMask, self.eventMask)    
