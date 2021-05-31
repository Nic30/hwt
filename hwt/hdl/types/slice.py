from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType


class HSlice(HdlType):
    """
    Slice type, used for selecting items from arrays or vectors
    """

    @internal
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.sliceVal import HSliceVal
            cls._valCls = HSliceVal
            return cls._valCls
