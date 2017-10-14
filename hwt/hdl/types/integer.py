from hwt.hdl.types.hdlType import HdlType


class Integer(HdlType):
    """
    Hdl integer type
    """

    def __eq__(self, other):
        return type(self) == type(other)

    def __hash__(self):
        return hash(type(self))

    def all_mask(self):
        return 1

    @classmethod
    def get_auto_cast_fn(cls):
        from hwt.hdl.types.integerCast import cast_integer
        return cast_integer

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.integerVal import IntegerVal
            cls._valCls = IntegerVal
            return cls._valCls
