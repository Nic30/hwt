from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType


class HString(HdlType):

    def all_mask(self):
        return 1

    @internal
    @classmethod
    def getConstCls(cls):
        try:
            return cls._constCls
        except AttributeError:
            from hwt.hdl.types.stringConst import HStringConst
            cls._constCls = HStringConst
            return cls._constCls
