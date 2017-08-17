from hwt.hdlObjects.types.hdlType import HdlType


class Integer(HdlType):
    """
    Hdl integer type
    """

    def __eq__(self, other):
        return (
                type(self) == type(other)
               )

    def __hash__(self):
        return hash(type(self))

    def all_mask(self):
        return 1

    @classmethod
    def get_auto_cast_fn(cls):
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
