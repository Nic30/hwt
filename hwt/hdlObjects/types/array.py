from hwt.hdlObjects.types.hdlType import HdlType
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.serializer.serializerClases.indent import getIndent


class Array(HdlType):
    """
    vldMask and eventMask on Array_val instance is not used instead of that
    these flags on elements are used
    """
    def __init__(self, elmType, size):
        super(Array, self).__init__()
        self.elmType = elmType
        self.size = size

    def __hash__(self):
        return hash((self.elmType, self.size))

    def bit_length(self):
        try:
            itemSize = self.elmType.bit_length
        except AttributeError:
            itemSize = None
        if itemSize is None:
            raise TypeError("Can not determine size of array because item has not determinable size")

        s = self.size
        if isinstance(s, RtlSignalBase):
            s = s.staticEval()
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
        :param withAddr: if is not none is used as a additional information about where
            on which address this type is stored (used only by HStruct)
        :param expandStructs: expand HStruct types (used by HStruct and Array)
        """

        return "%s<HdlType %s of\n%s[%r]>" % (getIndent(indent),
                                              self.__class__.__name__,
                                              self.elmType.__repr__(indent=indent + 1,
                                                                    withAddr=withAddr,
                                                                    expandStructs=expandStructs),
                                              self.size)
