from hwt.hdl.assignment import Assignment
from hwt.hdl.variables import SignalItem
from hwt.serializer.generic.indent import getIndent


class DebugTmpVarStack():
    """
    Collect tmp variables in serialization and format them to readable form

    .. code-block:: python
        tmpVars = DebugTmpVarStack()
        ctx = VhdlSerializer.getBaseContext()
        ctx.createTmpVarFn = tmpVars.createTmpVarFn
        s = VhdlSerializer.Assignment(self, ctx)
        "%s%s" % (tmpVars.serialize(), s)

    """
    def __init__(self, serializer):
        """
        :ivar vars: list of serialized variable declarations
        """
        self.vars = []
        self.serializer = serializer
        self.ctx = self.serializer.getBaseContext()

    def createTmpVarFn(self, suggestedName, dtype):
        # [TODO] it is better to use RtlSignal
        ser = self.serializer
        s = SignalItem(suggestedName, dtype, virtualOnly=True)
        s.hidden = False
        serializedS = ser.SignalItem(s, self.ctx, declaration=True)
        self.vars.append((serializedS, s))

        return s

    def _serializeItem(self, item):
        var, s = item
        # assignemt of value for this tmp variable
        a = Assignment(s.defaultVal, s, virtualOnly=True)
        return "%s\n%s" % (var, self.serializer.Assignment(a, self.ctx))

    def serialize(self, indent=0):
        if not self.vars:
            return ""

        separator = getIndent(indent) + "\n"
        return separator.join(map(self._serializeItem, self.vars)) + "\n"
