from vhdl_toolkit.synthetisator.exceptions import TypeConversionErr, SerializerException

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
    __slots__ = ['name', 'valueCls']
    """
    Hdl type container
    @cvar Ops: class with defined operators for values derived from this type  
    """
    def __init__(self):
        self.name = None
        #self.ValueCls = None
        self.constrain = None
    
    def __eq__(self, other):
        return type(self) is type(other)
    
    def __hash__(self):
        return hash((self.name, self.constrain))
    
    def convert(self, sigOrVal, toType):
        if sigOrVal.dtype == toType:
            return sigOrVal
        else:
            raise TypeConversionErr("Conversion of type %s to type %s is not implemented" % (repr(self), repr(toType)))
    
    def valAsVhdl(self, val, serializer):
        raise SerializerException("Serialization of type %s is not implemented" % (repr(self)))

    def __repr__(self):
        return "<HdlType %s>" % (self.__class__.__name__)
