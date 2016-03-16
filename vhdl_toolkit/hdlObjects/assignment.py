class Assignment():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def __repr__(self):
        from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    


class MapExpr():
    def __init__(self, compSig, value):
        self.compSig = compSig 
        self.value = value

    def __repr__(self):
        from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.MapExpr(self)