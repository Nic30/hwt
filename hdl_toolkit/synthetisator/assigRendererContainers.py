class DepContainer():
    def __init__(self):
        self.pos = set()  # if cond
        self.neg = set()  # if not cond
        
    def __repr__(self):
        return "<DepContainer pos:%s, neg:%s>" % (repr(self.pos), repr(self.neg))

class IfTreeNode():
    """
    
    @ival neg: dict condition : IfTreeNode object
    @ivar negSt: statements which will happen if condition is not met
    
    """
    def __init__(self, cond):
        self.cond = cond
        self.pos = []
        self.neg = []



