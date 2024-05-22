from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.types.hdlType import HdlType


class HFunction(HdlType):
    """
    A type which represent reference to HDL function.
    """

    def all_mask(self):
        return 1

    @internal
    @classmethod
    def getConstCls(cls):
        return HFunctionConst


class HFunctionConst(HConst):
    pass
