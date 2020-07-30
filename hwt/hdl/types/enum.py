from hwt.hdl.types.hdlType import HdlType
from hwt.doc_markers import internal


# [TODO] use python enum and only emulate HDL enum for HDL
class HEnum(HdlType):
    """
    Hdl enum type

    :ivar ~.name: name of this type
    :ivar ~._allValues: tuple of all values for this enum
    :note: for each value there is a property on this type object
    """

    def __init__(self, name, valueNames, const=False):
        """
        :param name: name for this type
        :param valueNames: sequence of string which will be used as names
            for enum members
        """
        super(HEnum, self).__init__(const=const)
        self.name = name
        self._allValues = tuple(valueNames)
        for name in valueNames:
            v = self.from_py(name)
            assert not hasattr(self, name)
            setattr(self, name, v)

    def all_mask(self):
        return 1

    def bit_length(self):
        return len(self._allValues).bit_length()

    @internal
    def domain_size(self):
        """
        :return: how many values can have specified type
        """
        return int(2 ** self.bit_length())

    @internal
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.enumVal import HEnumVal
            cls._valCls = HEnumVal
            return cls._valCls
