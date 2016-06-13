from hdl_toolkit.hdlObjects.types.hdlType import HdlType 

class Boolean(HdlType):
    def __init__(self):
        super().__init__()
        self.name = 'boolean'
    
    def valAsVhdl(self, val, serializer):
        return str(bool(val.val))

    @classmethod
    def getConvertor(cls):
        from hdl_toolkit.hdlObjects.types.booleanConversions import convertBoolean
        return convertBoolean

    def bit_length(self):
        return 1
    
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hdl_toolkit.hdlObjects.types.booleanVal import BooleanVal 
            cls._valCls = BooleanVal
            return cls._valCls