from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType


class Slice(HdlType):
    """
    Slice type, used for selecting items from arrays or vectors
    """

    @internal
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.sliceVal import SliceVal
            cls._valCls = SliceVal
            return cls._valCls
