from vhdl_toolkit.hdlObjects.specialValues import Unconstrained
class Bitmask():
    
    @staticmethod
    def mask(bits):
        return (1 << bits) - 1
    
    @staticmethod
    def bitField(_from, to):
        """
        _from 0 to 1 -> '1'  
        """
        w = to - _from
        return Bitmask.mask(w) << _from
    
    @staticmethod
    def extendWithSet(mask, actualWidth, toWidth):    
        return Bitmask.bitField(actualWidth - 1, toWidth) | mask
    
class Value():
    """
    Wrap around hdl value with overloaded operators
    http://www.rafekettler.com/magicmethods.html
    
    """
    def __init__(self, val, widthOrType, vldMask, eventMask=0):
        if isinstance(val, Value):
            val = val.val
        assert(val is None or isinstance(val, int) or isinstance(val, bool) 
               or isinstance(val, str) or isinstance(val, float) or isinstance(val, Value))
        
        self.val = val
        self.widthOrType = widthOrType
        self.vldMask = vldMask
        self.eventMask = eventMask
    
    @staticmethod
    def convertVal(val, toT):
        if val.widthOrType == toT:
            return val.clone()
        fromW = val.widthOrType
        if toT == int:
            if fromW == bool:
                m = 1
                return Value(int(val.val), toT, val.vldMask, val.eventMask)
            elif isinstance(fromW, int):
                v = val.clone()
                m = Value.widthFromWidthOrType(toT, v)
                v.vldMask &= m
                v.eventMask &= m 
                v.widthOrType = toT
                return v
            else:
                raise NotImplementedError()
        elif isinstance(toT, int):
            m = Bitmask.mask(toT)
            if isinstance(fromW, int):
                v = val.clone()
                v.val = v.val & m 
                v.vldMask = m if v.vldMask else 0
                v.eventMask = m if v.eventMask else 0   
                v.widthOrType = toT
                return v
            elif fromW == int:
                return Value(int(val.val & m), toT,
                              m if val.vldMask else 0,
                              m if val.eventMask else 0)
                
            elif fromW == bool:
                return Value(int(val.val), toT,
                              m if val.vldMask else 0,
                              m if val.eventMask else 0)
            else:
                raise NotImplementedError("Can not convert %s to %s" % (str(fromW), str(toT)))
        elif toT == bool:
            return Value(bool(val.val), toT,
                         1 if val.isCompletlyValid() else 0,
                         1 if val.eventMask else 0)
        elif toT == Unconstrained:
            v = Value.convertVal(val, int)
            v.widthOrType = Unconstrained
            return v
        else:
            raise NotImplementedError("Conversion to %s was not implemented yet" % (str(toT)))
        
    @classmethod
    def fromVal(cls, val, widthOrType):
        if val == None:
            vldMask = 0
        elif isinstance(val, Value):
            return Value.convertVal(val, widthOrType)
        else:
            vldMask = Bitmask.mask(Value.widthFromWidthOrType(widthOrType, val))
        return cls(val, widthOrType, vldMask)
    
    def clone(self):
        return Value(self.val, self.widthOrType, self.vldMask, eventMask=self.eventMask)
    
    @staticmethod
    def widthFromWidthOrType(widthOrType, val):
        if isinstance(widthOrType, int):
            return widthOrType
        elif widthOrType == bool:
            return 1
        elif widthOrType == int:
            if val is None:
                w = 1
            else:
                w = val.bit_length()
            return max([1, w])
        elif widthOrType == str:
            return len(val)
        elif widthOrType == Unconstrained:
            w = widthOrType.derivedWidth
            if not isinstance(w, int):
                raise TypeError("Width was not derived")
            return w
        else:
            raise NotImplementedError("widthFromWidthOrType not implemented for %s (%s)" % (str(widthOrType), str(widthOrType.__class__)))
    
    @staticmethod
    def widthAisBigger(a, b):
        if a == bool:
            return False
        elif b == bool:
            return True
        elif isinstance(a, int) and isinstance(b, int):
            return a > b
        elif a == int and b == int:
            return False
        else:
            raise NotImplementedError()
        
        
    @staticmethod
    def smallerWidth(a, b):
        return b if Value.widthAisBigger(a, b) else a
    
    @staticmethod
    def biggerWidth(a, b):
        return a if Value.widthAisBigger(a, b) else a
        
       
    def isCompletlyValid(self):
        return self.vldMask == Bitmask.mask(Value.widthFromWidthOrType(self.widthOrType, self.val))

    def __eq__(self, other):
        """
        @attention: ignores eventMask
        """
        if isinstance(other, Value):
            eq = self.val == other.val \
            and self.isCompletlyValid() and other.isCompletlyValid()
            vldMask = int(self.isCompletlyValid() and other.isCompletlyValid())
            evMask = int(self.eventMask & other.eventMask)
            # and self.eventMask == other.eventMask
        else:
            eq = self.val == other and self.isCompletlyValid()
            vldMask = int(self.isCompletlyValid())
            evMask = int(bool(self.eventMask))
        return Value(eq, bool, vldMask, eventMask=evMask)
    def __ne__(self, other):
        return not self.__eq__(other)
    
        
    def __lt__(self, other):
        raise NotImplementedError()
        
    def ___le__(self, other):
        raise NotImplementedError()
    
    def __gt__(self, other):
        raise NotImplementedError()
    
    def __ge__(self, other):
        raise NotImplementedError()
    # arithmetic
    def __add__(self, other):
        def isIntOrVector(typ):
            return isinstance(typ, int) or typ == int
            
        if not isinstance(other, Value):
            other = Value.fromVal(other, other.__class__)
        if not isIntOrVector(self.widthOrType) and isIntOrVector(other.widthOrType):
            raise TypeError("Value.__add__ was not yet implemented for self.widthOrType %s, other.widthOrType %s" % (str(self.widthOrType), str(other.widthOrType)))  # otherwise not implemented
        v = self.val + other.val
        w = self.widthOrType
        if w == int or  isinstance(w, int):
            # extendMasks integers are not synthetisable types, they can not became invalid
            w = Value.widthFromWidthOrType(self.widthOrType, v)
            vldMask = Bitmask.mask(w)
            if self.eventMask or other.eventMask:
                eventMask = vldMask
            else:
                eventMask = 0
            
        else:
            vldMask = self.vldMask & other.vldMask
            raise NotImplementedError("Value.__add__ was not implemented for %s and %s yet" 
                                      % (str(w), str(other.widthOrType)))
        
        # [TODO] carry
        return Value(
            v, w, vldMask,
            eventMask=eventMask)
    
    def __sub__(self, other):
        return (-self) + other
    
    def __mul__(self, other):
        if not isinstance(other, Value):
            other = Value.fromVal(other, other.__class__)
        assert(self.widthOrType == other.widthOrType == int)
        val = self.val * other.val
        w = Value.biggerWidth(self.widthOrType, other.widthOrType)
        assert(w == int)
        vldMask = Bitmask.mask(val.bit_length())
        eventMask = vldMask if self.eventMask or other.eventMask else 0
        
        return Value(val, w, vldMask, eventMask=eventMask)
    
    def __div__(self, other):
        if not isinstance(other, Value):
            other = Value.fromVal(other, other.__class__)
        assert(self.widthOrType == other.widthOrType == int)
        val = self.val // other.val
        w = self.widthOrType
        assert(w == int)
        vldMask = Bitmask.mask(val.bit_length())
        eventMask = vldMask if self.eventMask or other.eventMask else 0
        
        return Value(val, w, vldMask, eventMask=eventMask)
        

    
    def __neg__(self):
        v = self.clone()
        if self.widthOrType == bool:
            v.val = not v.val
        else:
            v.val = -v.val
        return v

    # logic
    def __and__(self, other):
        if isinstance(other, Value):
            v = bool(self.val) & bool(other.val)
            return Value(
                v,
                Value.smallerWidth(self.widthOrType, other.widthOrType),
                self.vldMask & other.vldMask,
                self.eventMask | other.eventMask)
        else:
            v = self.val & other
            return Value(
                v,
                self.widthOrType,
                self.vldMask,
                self.eventMask)
    
    # __nonzero in python2x
    def __bool__(self):
        return bool(self.val)
    def asVhdl(self):
        w = self.widthOrType
        if w == bool or w == int or w == str:
            assert(self.vldMask)
            assert(not self.eventMask)
            if w == str:
                return '"%s"' % (self.val)
            else:
                return str(self.val)
        elif isinstance(w, int):
            v = "X"
            if w == 1:
                return "'%s'" % (v) 
            elif w % 4 == 0:
                return ('X"%0' + str(w % 4) + 'x"') % (self.val)
            else:
                return ('B"{0:0' + str(w) + 'b}"').format(self.val)
        else:
            raise NotImplementedError()
    def __repr__(self):
        return "<Value {0:s}, vldMask {1:b}, eventMask {2:b}>".format(
                    str(self.val), self.vldMask, self.eventMask)    
