from hwt.hdl.types.hdlType import HdlType


class HBool(HdlType):

    def __eq__(self, other):
        return type(self) is type(other)

    def __hash__(self):
        return hash(HBool)

    @classmethod
    def get_auto_cast_fn(cls):
        from hwt.hdl.types.boolCast import cast_hbool
        return cast_hbool

    def bit_length(self):
        return 1

    def all_mask(self):
        return 1

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.boolVal import HBoolVal
            cls._valCls = HBoolVal
            return cls._valCls
