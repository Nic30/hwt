from hwt.hdlObjects.types.hdlType import HdlType
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class Array(HdlType):
    """
    vldMask and eventMask on Array_val instance is not used instead of that
    these flags on elements are used
    """
    def __init__(self, elmType, size):
        super(Array, self).__init__()
        self.elmType = elmType
        self.size = size

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.elmType == other.elmType and
            self.size == other.size
            )

    def __hash__(self):
        return hash((self.elmType, self.size))

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
            from hwt.hdlObjects.types.arrayVal import ArrayVal
            cls._valCls = ArrayVal
            return cls._valCls

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
