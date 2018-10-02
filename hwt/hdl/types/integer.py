from hwt.hdl.types.hdlType import HdlType
from hwt.doc_markers import internal


class Integer(HdlType):
    """
    Hdl integer type
    """

    def __eq__(self, other):
        return type(self) == type(other)

    @internal
    def __hash__(self):
        return hash(type(self))

    def all_mask(self):
        return 1

    @internal
    def domain_size(self):
        """
        :return: how many values can have specified type
        """
        return 1 << 32

    @internal
    @classmethod
    def get_auto_cast_fn(cls):
        from hwt.hdl.types.integerCast import cast_integer
        return cast_integer

    @internal
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.integerVal import IntegerVal
            cls._valCls = IntegerVal
            return cls._valCls
