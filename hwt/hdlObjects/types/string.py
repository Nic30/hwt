from hwt.hdlObjects.types.hdlType import HdlType


class String(HdlType):
    def __init__(self):
        super().__init__()
        self.name = "STRING"

    def all_mask(self):
        return 1

    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.stringVal import StringVal
            cls._valCls = StringVal
            return cls._valCls
