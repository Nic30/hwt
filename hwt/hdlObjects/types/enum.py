from hwt.hdlObjects.types.hdlType import HdlType


class Enum(HdlType):
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
        super(Enum, self).__init__()
        self.name = name
        self._allValues = tuple(valueNames)
        for n in valueNames:
            v = self.fromPy(n)
            setattr(self, n, v)

    def __hash__(self):
        return hash((self.name, self._allValues))

    def all_mask(self):
        return 1

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.enumVal import EnumVal
            cls._valCls = EnumVal
            return cls._valCls
