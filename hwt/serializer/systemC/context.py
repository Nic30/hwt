from copy import copy


class SystemCCtx(): # VerilogSerializerCtx
    """
    Context of SystemC serializer

    :ivar ~.isTarget: specifies if current expression is part of target
        (= do not add .read())
    :ivar ~.isSensitivityList: flag that specifies if serializer is
        in sensitivity list scope and signals are allowed
        to use event operators
    """

    def __init__(self, *args, **kwargs):
        super(SystemCCtx, self).__init__(*args, **kwargs)
        self.isTarget = False
        self.isSensitivityList = False

    def forTarget(self):
        c = copy(self)
        c.isTarget = True
        return c

    def forSensitivityList(self):
        c = copy(self)
        c.isTarget = True
        c.isSensitivityList = True
        return c
