

class ReturnCalled(Exception):
    def __init__(self, val):
        self.val = val

class ReturnContainer():
    def __init__(self, val=None):
        self.val = val

    def seqEval(self):
        raise ReturnCalled(self.val.staticEval())       

#def evalCond(cond):
#    _cond = True
#    assert isinstance(cond, set)
#    for c in cond:
#        _cond = _cond and bool(c.staticEval())
#        
#    return _cond

def simEvalCond(cond, simulator):
    _cond = True
    _vld = 1
    for c in cond:
        v = c.simEval(simulator)
        _cond = _cond and bool(v.val)
        assert isinstance(v.vldMask, int)
        _vld &= v.vldMask
        
    return _cond, _vld



class IfContainer():
    """
    Structural container for hdl rendering
    """
    def __init__(self, cond, ifTrue=[], ifFalse=[], elIfs=[]):
        self.cond = cond
        self.ifTrue = ifTrue
        self.elIfs = elIfs
        self.ifFalse = ifFalse
        
    @staticmethod
    def evalCase(simulator, stm, condVld):
        for r in stm.simEval(simulator):
            if not condVld:
                r[1].vldMask = 0
            yield r
    
    def simEval(self, simulator):
        """
        Same like seqEval but does not assign to signal instead of
        yield tuple (signal, value)
        """
        condRes, condVld = simEvalCond(self.cond, simulator)
        if condRes or not condVld:
            for stm in self.ifTrue:
                yield from IfContainer.evalCase(simulator, stm, condVld)
        else:
            for c in self.elIfs:
                subCondRes, subCondVld = simEvalCond(c[0], simulator)
                if subCondRes:
                    for stm in c[1]:
                        yield from IfContainer.evalCase(simulator, stm, subCondVld)
                    raise StopIteration()
            
            for stm in self.ifFalse:
                yield from IfContainer.evalCase(simulator, stm, condVld)
        
    #def seqEval(self):
    #    # [TODO] use simEval and then 
    #    if evalCond(self.cond):
    #        for s in self.ifTrue:
    #            s.seqEval()
    #    else:
    #        for c in self.elIfs:
    #            if evalCond(c[0]):
    #                for s in c[1]:
    #                    s.seqEval()
    #                return
    #        
    #        for s in self.ifFalse:
    #            s.seqEval()
        
    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.IfContainer(self)

class SwitchContainer():
    """
    Structural container for hdl rendering
    """
    def __init__(self, switchOn, cases):
        self.switchOn = switchOn
        self.cases = cases
    def simEval(self, simulator):
        raise NotImplementedError()
    def seqEval(self):
        raise NotImplementedError()
    def __repr__(self):
        from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.SwitchContainer(self)
 
class WhileContainer():
    """
    Structural container for hdl rendering
    """
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    
    def simEval(self, simulator):
        raise NotImplementedError()
    
    def seqEval(self):
        while True:
            cond = True
            for c in self.cond:
                cond = cond and bool(c.staticEval())
            if not cond:
                break
            
            for s in self.body:
                s.seqEval()
