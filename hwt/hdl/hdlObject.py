

class HdlObject():
    """
    Base Hdl object class for object which can be directly serialized
    to target HDL language
    """

    def __repr__(self):
        from hwt.serializer.hwt.serializer import HwtSerializer
        ctx = HwtSerializer.getBaseContext()
        return getattr(HwtSerializer, self.__class__.__name__)(self, ctx)
