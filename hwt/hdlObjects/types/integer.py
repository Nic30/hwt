from hwt.hdlObjects.types.hdlType import HdlType 


class Integer(HdlType):
    
    def __init__(self, _min=None, _max=None):
        super(Integer, self).__init__()
        self.min = _min
        self.max = _max
    
    def __eq__(self, other):
        return self is other or (
            type(self) == type(other) and self.max == other.max and self.min == other.min
                                 )
    def __hash__(self):
        return hash((self.max, self.min))
    
    def all_mask(self):
        return 1

    @classmethod
    def getConvertor(cls):
        from hwt.hdlObjects.types.integerConversions import convertInteger
        return convertInteger
    
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.integerVal import IntegerVal 
            cls._valCls = IntegerVal
            return cls._valCls