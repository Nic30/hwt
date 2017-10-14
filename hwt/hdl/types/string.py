from hwt.hdl.types.hdlType import HdlType


class String(HdlType):
    def __init__(self):
        super().__init__()

    def all_mask(self):
        return 1

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdl.types.stringVal import StringVal
            cls._valCls = StringVal
            return cls._valCls
