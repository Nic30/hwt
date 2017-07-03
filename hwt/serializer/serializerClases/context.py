
class SerializerCtx():
    """
    Serializer context

    :ivar scope: instance of NameScope used to check id availability
    :ivar indent: number of visual indentations for code in this context
    :ivar createTmpVarFn: function (sugestedName, dtype) returns variable
        this function will be called to create tmp variables
    :ivar constCache: constant cache to extract frequently used large constant values
        from code (visual improvement)
    """

    def __init__(self, scope, indent, createTmpVarFn, constCache=None):
        self.scope = scope
        self.indent = indent
        self.createTmpVarFn = createTmpVarFn
        self.constCache = constCache

    def withIndent(self, indent=1):
        return SerializerCtx(self.scope, self.indent + indent, self.createTmpVarFn, self.constCache)
    
