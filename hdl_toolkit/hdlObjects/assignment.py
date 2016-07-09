class Assignment():
    """
    Assignment container
    @ivar src: source  
    @ivar dest: destination signal
    @ivar cond: set of terms if all them are evaluated to True,
                assignment is active
    @ivar condRes: tmp variable for simPropagateChanges
    """
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.cond = set()
        
    def seqEval(self):
        self.dst._val = self.src.staticEval() 
    
    def simEval(self, simulator):
        yield (self.dst, self.src.simEval(simulator))
        
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    

class MapExpr():
    """
    Map expression, is used in component instance mapping
    """
    def __init__(self, compSig, value):
        self.compSig = compSig 
        self.value = value

    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.MapExpr(self)
