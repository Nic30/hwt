from hwt.synthesizer.exceptions import TypeConversionErr


class InvalidVHDLTypeExc(Exception):
    def __init__(self, vhdlType):
        self.vhdlType = vhdlType
    
    def __str__(self):    
        variableName = self.variable.name
        return "Invalid type, width is %s in the context of variable %s" \
            % (str(self.vhdlType.getWidth()), variableName)

    def __repr__(self):
        return self.__str__()

class HdlType():
    #_slots__ = ['name', "constrain", "_valCls", "_convertor"]

    def __init__(self):
        self.constrain = None
        
    def __eq__(self, other):
        return type(self) is type(other)
    
    def __hash__(self):
        return hash((self.name, self.constrain))
    
    def fromPy(self, v):
        return self.getValueCls().fromPy(v, self)
    
    def convert(self, sigOrVal, toType):
        if sigOrVal._dtype == toType:
            return sigOrVal
        
        try:
            c = self._convert
        except AttributeError:
            c = self.getConvertor()
            self._convertor = c

        return c(self, sigOrVal, toType)
    
    @classmethod
    def getConvertor(cls):
        return HdlType.defaultConvert
    
    def defaultConvert(self, sigOrVal, toType):
        raise TypeConversionErr("Conversion of %r of type \n%r to type %r is not implemented" 
                                   % (sigOrVal, self, toType))
    
    def __repr__(self):
        return "<HdlType %s>" % (self.__class__.__name__)
