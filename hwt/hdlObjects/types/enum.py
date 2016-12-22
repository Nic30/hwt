from hwt.hdlObjects.types.hdlType import HdlType 

class Enum(HdlType):
    def __init__(self, name, valueNames):
        super(Enum, self).__init__()
        self.name = name
        self._allValues = valueNames
        for n in valueNames:
            v = self.fromPy(n)
            setattr(self, n, v)
    
    def _add(self, name):
        """
        Add member of the enum
        """
        self._allValues.append(name)
        v = self.fromPy(name)
        setattr(self, name, v)
        return v
    
    def all_mask(self):
        return 1
    
    @classmethod
    def getValueCls(cls):
        try:
            return cls._valCls
        except AttributeError:
            from hwt.hdlObjects.types.enumVal import EnumVal 
            cls._valCls = EnumVal
            return cls._valCls