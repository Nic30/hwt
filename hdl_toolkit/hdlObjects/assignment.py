from hdl_toolkit.simulator.utils import valueHasChanged


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
        self.isEventDependent = False
        self.cond = set()
        
    def seqEval(self):
        self.dst._val = self.src.staticEval() 
    
    def simEval(self, simulator):
        """
        @return: generator of tuple (dst, valueUpdater, isEventDependent)
        """
        nextVal = self.src.simEval(simulator)
        updater = lambda currentVal: (valueHasChanged(currentVal, nextVal), nextVal)
        yield (self.dst, updater, self.isEventDependent)
        
    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    

