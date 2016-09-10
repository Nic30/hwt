from hdl_toolkit.simulator.utils import valueHasChanged

def mkUpdater(nextVal):
    """
    Create value updater for simulation
    """
    return lambda currentVal: (valueHasChanged(currentVal, nextVal), nextVal)

def mkArrayUpdater(simulator, nextItemVal, indexes):
    """
    Create value updater for simulation for value of array type 
    """
    _indexes = list(map(lambda i: i.simEval(simulator), indexes))
     
    def updater(currentVal):
        if len(_indexes) > 1:
            raise NotImplementedError()
        
        index = _indexes[0]
        change = valueHasChanged(currentVal[index], nextItemVal)
        currentVal[index] = nextItemVal
        return (change, currentVal)
    
    return updater
    

class Assignment(object):
    """
    Assignment container
    @ivar src: source  
    @ivar dest: destination signal
    @ivar cond: set of terms if all them are evaluated to True,
                assignment is active
    @ivar indexes: description of index selector on dst (list of Index/Slice objects)
                    (f.e. [[0], [1]] means  dst[0][1]  )
    
    @cvar __instCntr: counter used for generating instance ids
    @ivar _instId: internaly used only for intuitive sorting of statements
    """
    __instCntr = 0
    
    def __init__(self, src, dst, indexes=None):
        self.src = src
        self.dst = dst
        self.isEventDependent = False
        self.indexes = indexes
        self.cond = set()
        self._instId = Assignment._nextInstId()
        
        dst.ctx.startsOfDataPaths.add(self)
    
    @classmethod
    def _nextInstId(cls):
        """
        Get next instance id
        """
        i = cls.__instCntr
        cls.__instCntr += 1
        return i
        
    def seqEval(self):
        self.dst._val = self.src.staticEval() 
    
    def simEval(self, simulator):
        """
        @return: generator of tuple (dst, valueUpdater, isEventDependent)
        """
        nextVal = self.src.simEval(simulator)
        
        if self.indexes:
            updater = mkArrayUpdater(simulator, nextVal, self.indexes)
        else:
            updater = mkUpdater(nextVal)
        yield (self.dst, updater, self.isEventDependent)
    
    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    

