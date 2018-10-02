from hwt.serializer.generic.context import SerializerCtx


class ValueWidthRequirementScope():
    """
    Context manager which temporarily swaps the _valueWidthRequired on specified context 
    """
    def __init__(self, ctx, val):
        self.ctx = ctx
        self.val = val

    def __enter__(self):
        self.oldVal = self.ctx._valueWidthRequired
        self.ctx._valueWidthRequired = self.val

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ctx._valueWidthRequired = self.oldVal


class HwtSerializerCtx(SerializerCtx):
    def __init__(self, scope, indent: int, createTmpVarFn, constCache=None):
        SerializerCtx.__init__(self, scope, indent,
                               createTmpVarFn, constCache=constCache)
        self._valueWidthRequired = False

    def valWidthReq(self, val):
        """
        Create scope where width is required on values or not

        .. code-block:: python

            with ctx.valWidthReq(True):
               #...
        """
        return ValueWidthRequirementScope(self, val)
