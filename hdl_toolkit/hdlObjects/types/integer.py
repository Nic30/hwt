from hdl_toolkit.hdlObjects.types.hdlType import HdlType 
from hdl_toolkit.serializer.exceptions import SerializerException

class Integer(HdlType):
    
    def __init__(self, _min=None, _max=None):
        super(Integer, self).__init__()
        self.min = _min
        self.max = _max

    def valAsVhdl(self, val, serializer):
        return str(int(val.val))
    
    def __eq__(self, other):
        return self is other or (
            type(self) == type(other) and self.max == other.max and self.min == other.min
                                 )
    def __hash__(self):
        return hash((self.max, self.min))
    
    def all_mask(self):
        return 1
    
    @property
    def name(self):
        ma = self.max
        mi = self.min
        noMax = ma is None
        noMin = mi is None
        if noMin: 
            if noMax:
                return "INTEGER"
            else:
                raise SerializerException("If max is specified min has to be specified as well")
        else:
            if noMax:
                if mi == 0:
                    return "NATURAL"
                elif mi == 1:
                    return "POSITIVE"
                else:
                    raise SerializerException("If max is specified min has to be specified as well")
            else:
                return "INTEGER RANGE %d to %d" % (mi, ma)

    @classmethod
    def getConvertor(cls):
        from hdl_toolkit.hdlObjects.types.integerConversions import convertInteger
        return convertInteger
    
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hdl_toolkit.hdlObjects.types.integerVal import IntegerVal 
            cls._valCls = IntegerVal
            return cls._valCls