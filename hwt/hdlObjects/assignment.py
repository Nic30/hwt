
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
    
    def __init__(self, src, dst, indexes=None, virtualOnly=False):
        """
        @param dst: destination to assign to
        @param src: source which is assigned from
        @param indexes: description of index selector on dst (list of Index/Slice objects)
                (f.e. [[0], [1]] means  dst[0][1]  )
        @param virtualOnly: flag indicates that this assignments is only virtual and should not be added into
                netlist, because it is only for internal notation
        """
        self.src = src
        self.dst = dst
        self.isEventDependent = False
        self.indexes = indexes
        self.cond = set()
        self._instId = Assignment._nextInstId()
        
        if not virtualOnly:
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
        """Sequentially evaluate this assignment"""
        self.dst._val = self.src.staticEval() 
    
    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer, onlyPrintDefaultValues
        return VhdlSerializer.Assignment(self, onlyPrintDefaultValues)    

