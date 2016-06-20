from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.hdlObjects.types.integer import Integer 

class Slice(Array):
    def __init__(self):
        super().__init__(Integer(), 2)
        
    def valAsVhdl(self, val, serializer):
        return "%s DOWNTO %s" % (serializer.Value(val.val[0]), serializer.Value(val.val[1]))

    def __hash__(self):
        return hash(self.constrain)

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hdl_toolkit.hdlObjects.types.sliceVal import SliceVal 
            cls._valCls = SliceVal
            return cls._valCls