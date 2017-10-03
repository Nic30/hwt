from hwt.hdl.types.hdlType import HdlType


class Boolean(HdlType):

    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(Boolean)

    @classmethod
    def get_auto_cast_fn(cls):
        from hwt.hdl.types.booleanCast import cast_boolean
        return cast_boolean

    def bit_length(self):
        return 1

    def all_mask(self):
        return 1

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.booleanVal import BooleanVal
            cls._valCls = BooleanVal
            return cls._valCls
