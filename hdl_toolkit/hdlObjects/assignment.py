from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.simulator.exceptions import SimNotInitialized
from hdl_toolkit.hdlObjects.value import Value


def hasDiferentVal(reference, sigOrVal):
    assert(isinstance(reference, Value))
    if isinstance(sigOrVal, Value):
        v = sigOrVal
    else:
        v = sigOrVal._val
    
    return reference != v

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
        
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.Assignment(self)    

    def evaluateCond(self):
        cond = None
        for c in self.cond:
            if cond is None:
                cond = c._val
            else:
                cond = cond & c._val
        
        return cond

    def simPropagateChanges(self):
        activeAsignments = []
        for d in self.dst.drivers:
            d.condRes = d.evaluateCond()
            if d.condRes is None or d.condRes.vldMask == 0 or bool(d.condRes.val):
                activeAsignments.append(d)
        
        l = len(activeAsignments)
        if l == 0:
            # print(">> %s disconnected"  % (repr(self)))
            # disconnected
            nextVal = self.dst._val.clone()
            nextVal.vldMask = 0
        elif l == 1:
            connectedTo = activeAsignments[0]
            # print(">> %s connected to: %s" % (repr(self), repr(connectedTo) ) )
            # connected
            nextVal = connectedTo.src
            if not isinstance(nextVal, Value):
                nextVal = nextVal._val.clone()
            if connectedTo.condRes and connectedTo.condRes.eventMask:
                nextVal.eventMask = Bitmask.mask(nextVal._dtype.bit_length())
        else:
            # connected to many
            # all has to be same or short circuit
            nextVal = None
            # print(">> %s multiple drivers: %s" % (repr(self), repr(activeAsignments) ) )
            for d in activeAsignments:
                if nextVal is None:
                    if isinstance(d.src, Value):
                        nextVal = d.src.clone()
                    else:
                        nextVal = d.src._val.clone()
                else:
                    if hasDiferentVal(nextVal, d.src):
                        nextVal.vldMask = 0

        try:
            sim = self._simulator
        except AttributeError:
            raise SimNotInitialized("Operator '%s' is not bounded to any simulator" % (str(self)))
        
        env = sim.env
        c = sim.config
        yield env.timeout(c.propagDelay(self))
        yield env.process(self.dst.simUpdateVal(nextVal))

class MapExpr():
    
    def __init__(self, compSig, value):
        self.compSig = compSig 
        self.value = value

    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return VhdlSerializer.MapExpr(self)
