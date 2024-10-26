from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.types.hdlType import HdlType
from hwt.pyUtils.typingFuture import override


class HFunction(HdlType):
    """
    A type which represent reference to HDL function.
    :note: For compatibility with HDL. It is not meant to be used
        as a function pointer to call a function in synthetisable code.
    """

    def all_mask(self):
        return 1

    @internal
    @override
    @classmethod
    def getConstCls(cls):
        return HFunctionConst


class HFunctionConst(HConst):
    pass
