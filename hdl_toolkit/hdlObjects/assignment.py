
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
    
    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    

