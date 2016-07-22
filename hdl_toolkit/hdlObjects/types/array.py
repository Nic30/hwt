from hdl_toolkit.hdlObjects.types.hdlType import HdlType 

class Array(HdlType):
    """
    vldMask and eventMask on Array_val instance is not used instead of that
    these flags on elements are used
    [TODO] Array in Array
    [TODO] Array elements should always be instance of Signal
           to prevent problems in simulation
    """
    def __init__(self, elmType, size):
        super(Array, self).__init__()
        self.elmType = elmType
        self.size = size
    
    def __hash__(self):
        return hash((self.elmType, self.size))
    
    def valAsVhdl(self, val, serializer):
        return  "(" + (",\n".join([serializer.Value(v) for v in val.val])) + ")"
    
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hdl_toolkit.hdlObjects.types.arrayVal import ArrayVal 
            cls._valCls = ArrayVal
            return cls._valCls