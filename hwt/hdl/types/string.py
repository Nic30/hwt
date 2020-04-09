from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType


class String(HdlType):

    def all_mask(self):
        return 1

    @internal
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.stringVal import StringVal
            cls._valCls = StringVal
            return cls._valCls
