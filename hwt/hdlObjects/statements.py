
class ReturnCalled(Exception):
    """
    Exception which is used as return statement while executing of hdl functions
    """
    def __init__(self, val):
        self.val = val

class ReturnContainer():
    """
    Stuctural container of return statement in hdl
    """
    
    def __init__(self, val=None):
        self.val = val

    def seqEval(self):
        raise ReturnCalled(self.val.staticEval())       

def seqEvalCond(cond):
    _cond = True
    for c in cond:
        _cond = _cond and bool(c.staticEval().val)
        
    return _cond

class IfContainer():
    """
    Structural container of if statement for hdl rendering
    """
    def __init__(self, cond, ifTrue=[], ifFalse=[], elIfs=[]):
        self.cond = cond
        self.ifTrue = ifTrue
        self.elIfs = elIfs
        self.ifFalse = ifFalse
        
    def seqEval(self):
        if seqEvalCond(self.cond):
            for s in self.ifTrue:
                s.seqEval()
        else:
            for c in self.elIfs:
                if seqEvalCond(c[0]):
                    for s in c[1]:
                        s.seqEval()
                    return
            
            for s in self.ifFalse:
                s.seqEval()
        
    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer, onlyPrintDefaultValues
        return VhdlSerializer.IfContainer(self, onlyPrintDefaultValues)

class SwitchContainer():
    """
    Structural container for switch statement for hdl rendering
    """
    def __init__(self, switchOn, cases):
        self.switchOn = switchOn
        self.cases = cases
    
    def seqEval(self):
        raise NotImplementedError()
    
    def __repr__(self):
        from hwt.serializer.vhdl.serializer import VhdlSerializer, onlyPrintDefaultValues
        return VhdlSerializer.SwitchContainer(self, onlyPrintDefaultValues)
 
class WhileContainer():
    """
    Structural container of while statement for hdl rendering
    """
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    
    def seqEval(self):
        while seqEvalCond(self.cond):
            for s in self.body:
                s.seqEval()

class WaitStm():
    """
    Structural container of wait statemnet for hdl rendering
    """
    def __init__(self, waitForWhat):
        self.isTimeWait = isinstance(waitForWhat, int)
        self.waitForWhat = waitForWhat
        
