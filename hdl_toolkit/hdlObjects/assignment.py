class Assignment():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def seqEval(self):
        self.dst._val = self.src.staticEval() 
        
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    


class MapExpr():
    def __init__(self, compSig, value):
        self.compSig = compSig 
        self.value = value

    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.MapExpr(self)
