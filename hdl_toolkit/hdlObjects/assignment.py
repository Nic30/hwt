from hdl_toolkit.simulator.utils import valueHasChanged

def mkUpdater(nextVal):
    return lambda currentVal: (valueHasChanged(currentVal, nextVal), nextVal)

def mkArrayUpdater(nextItemVal, index):
    def updater(currentVal):
        change = valueHasChanged(currentVal[index], nextItemVal)
        currentVal[index] = nextItemVal
        return (change, currentVal)
    
    return updater
    

class Assignment():
    """
    Assignment container
    @ivar src: source  
    @ivar dest: destination signal
    @ivar cond: set of terms if all them are evaluated to True,
                assignment is active
    @ivar condRes: tmp variable for simPropagateChanges
    @ivar indexes: description of index selector on dst (list of Index/Slice objects)
                    (f.e. [[0], [1]] means  dst[0][1]  )
    
    """
    def __init__(self, src, dst, indexes=None):
        self.src = src
        self.dst = dst
        self.isEventDependent = False
        self.indexes = indexes
        self.cond = set()
        
    def seqEval(self):
        self.dst._val = self.src.staticEval() 
    
    def simEval(self, simulator):
        """
        @return: generator of tuple (dst, valueUpdater, isEventDependent)
        """
        nextVal = self.src.simEval(simulator)
        
        yield (self.dst, mkUpdater(nextVal), self.isEventDependent)
        
    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    

