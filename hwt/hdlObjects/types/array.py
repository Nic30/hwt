from hwt.hdlObjects.types.hdlType import HdlType
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HArray(HdlType):
    """
    HDL array type

    :ivar elmType: type of elements
    :ivar size: number of items
    """
    def __init__(self, elmType, size):
        super(HArray, self).__init__()
        self.elmType = elmType
        self.size = size

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.size == other.size and
            self.elmType == other.elmType
            )

    def __hash__(self):
        return hash(id(self))

    def bit_length(self):
        """
        :return: bit width for this type
        """
        try:
            itemSize = self.elmType.bit_length
        except AttributeError:
            itemSize = None
        if itemSize is None:
            raise TypeError("Can not determine size of array because item has not determinable size")

        s = self.size
        if isinstance(s, RtlSignalBase):
            s = int(s.staticEval())
        return s * itemSize()

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.arrayVal import HArrayVal
            cls._valCls = HArrayVal
            return cls._valCls

    @classmethod
    def get_reinterpret_cast_fn(cls):
        from hwt.hdlObjects.types.arrayCast import reinterpret_cast_harray
        return reinterpret_cast_harray

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and Array)
        """
        return "%s[%r]" % (self.elmType.__repr__(indent=indent,
                                                 withAddr=withAddr,
                                                 expandStructs=expandStructs),
                           self.size)
