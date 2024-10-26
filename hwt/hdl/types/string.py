from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.pyUtils.typingFuture import override


class HString(HdlType):
    """
    :note: This type is meant for HwModule parameters, operations with this type are not synthetisable.
    """

    def all_mask(self):
        return 1

    @internal
    @override
    @classmethod
    def getConstCls(cls):
        try:
            return cls._constCls
        except AttributeError:
            from hwt.hdl.types.stringConst import HStringConst
            cls._constCls = HStringConst
            return cls._constCls

    @internal
    @override
    @classmethod
    def getRtlSignalCls(cls):
        try:
            return cls._rtlSignalCls
        except AttributeError:
            from hwt.hdl.types.stringConst import HStringRtlSignal
            cls._rtlSignalCls = HStringRtlSignal
            return cls._rtlSignalCls
