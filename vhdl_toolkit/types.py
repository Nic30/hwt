from vhdl_toolkit.hdlObjects.literal import Literal

class InvalidVHDLTypeExc(Exception):
    def __init__(self, vhdlType):
        self.vhdlType = vhdlType
    
    def __str__(self):    
        variableName = self.variable.name
        return "Invalid type, width is %s in the context of variable %s" \
            % (str(self.vhdlType.getWidth()), variableName)

    def __repr__(self):
        return self.__str__()


class VHDLType():
    __slots__ = ['width', 'min', 'name', 'ctx']
    """
    Vhdl type container
    """
    def __init__(self):
        self.width = None
        self.min = None
        self.name = None
        self.ctx = None
        
    def getWidth(self):
        if isinstance(self.width, type):
            self.width
        elif hasattr(self.width, "__call__"):
            w = self.width()
            if isinstance(w, list):
                return (Literal.get(w[0]) - Literal.get(w[1])) + 1
            return w
        return self.width
    
    def __repr__(self):
        return "<%s width:%s>" % (self.__class__.__name__, str(self.width))
        
class VHDLExtraType(object):
    """
    user type definition
    """
    @classmethod
    def createEnum(cls, name, values):
        self = cls()
        self.name = name
        self.values = set(values)
        return self
            
    def __repr__(self):
        return "<%s name:%s values:%s;" % (self.__class__.__name__, self.name, str(self.values))

    
    
