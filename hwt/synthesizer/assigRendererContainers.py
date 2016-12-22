
class IfTreeNode():
    """
    
    @ival neg: dict condition : IfTreeNode object
    @ivar negSt: statements which will happen if condition is not met
    
    """
    def __init__(self, cond):
        self.cond = cond
        self.pos = []
        self.neg = []



