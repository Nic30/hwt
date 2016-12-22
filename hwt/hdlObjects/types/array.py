from hwt.hdlObjects.types.hdlType import HdlType 

class Array(HdlType):
    """
    vldMask and eventMask on Array_val instance is not used instead of that
    these flags on elements are used
    """
    def __init__(self, elmType, size):
        super(Array, self).__init__()
        self.elmType = elmType
        self.size = size
    
    def __hash__(self):
        return hash((self.elmType, self.size))
    
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.arrayVal import ArrayVal 
            cls._valCls = ArrayVal
            return cls._valCls