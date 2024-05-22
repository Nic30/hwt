from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType


class HSlice(HdlType):
    """
    Slice type, used for selecting items from arrays or vectors
    """

    @internal
    @classmethod
    def getConstCls(cls):
        try:
            return cls._constCls
        except AttributeError:
            from hwt.hdl.types.sliceConst import HSliceConst
            cls._constCls = HSliceConst
            return cls._constCls
