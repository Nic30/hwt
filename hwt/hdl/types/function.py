from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import HValue


class HFunction(HdlType):
    """
    A type which represent reference to HDL function.
    """

    def all_mask(self):
        return 1

    @internal
    @classmethod
    def getValueCls(cls):
        return HFunctionVal


class HFunctionVal(HValue):
    pass
