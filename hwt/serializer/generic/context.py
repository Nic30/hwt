from copy import copy


class SerializerCtx():
    """
    Serializer context

    :ivar scope: instance of NameScope used to check id availability
    :ivar indent: number of visual indentations for code in this context
    :ivar createTmpVarFn: function (sugestedName, dtype) returns variable
        this function will be called to create tmp variables
    :ivar constCache: constant cache to extract frequently used large constant
        values from code (visual improvement)
    :ivar currentUnit: current Unit instance or None
    """

    def __init__(self,  scope, indent: int, createTmpVarFn, constCache=None):
        self.scope = scope
        self.indent = indent
        self.currentUnit = None

        if createTmpVarFn is None:
            self.createTmpVarFn = self.defaultCreateTmpVarFn
        else:
            self.createTmpVarFn = createTmpVarFn

        self.constCache = constCache

    def defaultCreateTmpVarFn(self, sugestedName, dtype):
        raise NotImplementedError()

    def withIndent(self, indent=1):
        """
        Create copy of this context with increased indent
        """
        ctx = copy(self)
        ctx.indent += indent
        return ctx
