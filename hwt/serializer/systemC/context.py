from hwt.serializer.serializerClases.context import SerializerCtx
from copy import copy


class SystemCCtx(SerializerCtx):
    """
    Context of SystemC serializer
    
    :ivar isTarget: specifies if current expression is part of target (= do not add .read())
    """
    def __init__(self, *args, **kwargs):
        super(SystemCCtx, self).__init__(*args, **kwargs)
        self.isTarget = False
        
    def forTarget(self):
        c = copy(self)
        c.isTarget = True
        return c