from hwt.hdlObjects.types.hdlType import HdlType


class HEnum(HdlType):
    """
    Hdl enum type

    :ivar name: name of this type
    :ivar _allValues: tuple of all values for this enum
    :note: for each value there is a property on this type object
    """

    def __init__(self, name, valueNames):
        """
        :param name: name for this type
        :param valueNames: sequence of string which will be used as names for enum
            members
        """
        super(HEnum, self).__init__()
        self.name = name
        self._allValues = tuple(valueNames)
        for name in valueNames:
            v = self.fromPy(name)
            assert not hasattr(self, name)
            setattr(self, name, v)

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return hash(id(self))

    def all_mask(self):
        return 1

    def bit_length(self):
        return len(self._allValues).bit_length()

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.enumVal import HEnumVal
            cls._valCls = HEnumVal
            return cls._valCls
