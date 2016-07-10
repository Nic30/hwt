class MapExpr():
    """
    Map expression, is used in component instance mapping
    """
    def __init__(self, compSig, value):
        self.compSig = compSig 
        self.value = value

    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.MapExpr(self)
