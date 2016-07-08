from hdl_toolkit.hdlObjects.types.hdlType import HdlType 

class String(HdlType):
    def __init__(self):
        super().__init__()
        self.name = "STRING"

    def valAsVhdl(self, val, serializer):
        return  '"%s"' % str(val.val)


    @classmethod
    def getConvertor(cls):
        from hdl_toolkit.hdlObjects.types.stringConversions import convertString
        return convertString
    

    def all_mask(self):
        return 1

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hdl_toolkit.hdlObjects.types.stringVal import StringVal 
            cls._valCls = StringVal
            return cls._valCls