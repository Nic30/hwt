from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class HArray(HdlType):
    """
    HDL array type

    :ivar ~.element_t: type of elements
    :ivar ~.size: number of items
    """

    def __init__(self, element_t, size, const=False):
        super(HArray, self).__init__(const=const)
        self.element_t = element_t
        self.size = size

    def __eq__(self, other):
        return self is other or (
            type(self) is type(other) and
            self.size == other.size and
            self.element_t == other.element_t
        )

    @internal
    def __hash__(self):
        return hash((self.const, self.element_t, self.size))

    def bit_length(self):
        """
        :return: bit width for this type
        """
        try:
            itemSize = self.element_t.bit_length
        except AttributeError:
            itemSize = None
        if itemSize is None:
            raise TypeError(
                "Can not determine size of array because item has"
                " not determinable size")

        s = self.size
        if isinstance(s, RtlSignalBase):
            s = int(s.staticEval())
        return s * itemSize()

    @internal
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.arrayVal import HArrayVal
            cls._valCls = HArrayVal
            return cls._valCls

    @internal
    @classmethod
    def get_reinterpret_cast_fn(cls):
        from hwt.hdl.types.arrayCast import reinterpret_cast_harray
        return reinterpret_cast_harray

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and Array)
        """
        return "%s[%r]" % (self.element_t.__repr__(indent=indent,
                                                 withAddr=withAddr,
                                                 expandStructs=expandStructs),
                           self.size)
