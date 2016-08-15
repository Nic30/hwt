from copy import deepcopy
import types

from hdl_toolkit.hdlObjects.specialValues import DIRECTION
from hdl_toolkit.hdlObjects.typeShortcuts import hInt, vec
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.synthesizer.interfaceLevel.interface.utils import walkPhysInterfaces
from hdl_toolkit.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.synthesizer.vectorUtils import getWidthExpr, fitTo


def _intfToSig(obj):
    if isinstance(obj, InterfaceBase):
        return obj._sig
    else:
        return obj

class StmCntx(list):
    """
    Base class of statement contexts
    """
    pass

def flaten(iterables):
    if isinstance(iterables, (list, tuple, types.GeneratorType)):
        for i in iterables:
            yield from flaten(i)
    else:
        yield iterables
        
class If(StmCntx):
    """
    Context of if statement
    
    @param cond: condition in if
    @param statements: list of statements which should be active if condition is met   
    """
    def __init__(self, cond, *statements):
        self.cond = _intfToSig(cond)
        self.elifConds = []
        self._appendStatements(set([self.cond,]), statements)
        
    def Else(self, *statements):
        ncond = set()
        ncond.add(~self.cond)
        
        for ec in self.elifConds:
            ncond.add(~ec)

        self._appendStatements(ncond, statements)
            
        # convert self to StmCntx to prevent any other else/elif
        stml = StmCntx()
        stml.extend(self)
        return stml
    
    def _appendStatements(self, condSet, statements):
        for stm in flaten(statements):
            for c in condSet:
                c.endpoints.append(stm)
            stm.cond.update(condSet)
            self.append(stm)
    
    def Elif(self, cond, *statements):
        cond = _intfToSig(cond)
        
        thisCond = set()
        thisCond.add(~self.cond)
        for c in self.elifConds:
            thisCond.add(~c)
        thisCond.add(cond)
        
        self._appendStatements(thisCond, statements)
        
        self.elifConds.append(cond)
        
        return self

class Switch(StmCntx):
    def __init__(self, switchOn):
        self.switchOn = switchOn
        self.cond = None
    
    _appendStatements = If._appendStatements
    
    def Case(self, caseVal, *statements):
        cond = self.switchOn._eq(caseVal)
        if self.cond is None:
            If.__init__(self, cond, *statements) 
        else:
            If.Elif(self, cond, *statements)
        return self
    
    def addCases(self, tupesValStmnts):
        s = self
        for val, statements in tupesValStmnts:
            if val is None:
                s = s.Default(*statements)
            else:
                s = s.Case(val, *statements)
        return s
    
    def Default(self, *statements):
        return If.Else(self, *statements)


def In(sigOrVal, iterable):
    res = None
    for i in iterable:
        i = toHVal(i)
        if res is None:
            res = sigOrVal._eq(i)
        else:
            res = res | sigOrVal._eq(i)

    return res

class FsmBuilder(StmCntx):
    """
    @ivar stateReg: register with state
    """
    
    def __init__(self, parent, stateT, stateRegName="st"):
        """
        @param parent: parent unit where fsm should be builded
        @param stateT: enum type of state
        @param stateRegName: name of register where sate is stored
        """
        self.stateReg = parent._reg(stateRegName, stateT, stateT.fromPy(stateT._allValues[0]))
        Switch.__init__(self, self.stateReg)
    
    _appendStatements = Switch._appendStatements
    def Trans(self, stateFrom, *condAndNextState):
        """
        @param stateFrom: apply when FSM is in this state
        @param condAndNextState: tupes (condition, newState),
                        last does not to have condition
        
        @attention: transitions has priority, first has the biggest 
        @attention: if stateFrom is None it is evaluated as default
        """
        top = None
        last = True
        
        for cAndS in reversed(condAndNextState):
            if last is True:
                last = False
                # if this is last trans. it does not have to condition
                try:
                    condition, newvalue = cAndS
                except TypeError:
                    top = c(cAndS, self.stateReg)
                    continue
                top = self.stateReg._same()

            else:
                condition, newvalue = cAndS
            
            # building decision tree    
            top =   If(condition,
                        c(newvalue, self.stateReg)
                    ).Else(
                        top
                    )
            
        # if there is no trans. this state fsm should hang in this state
        if not condAndNextState:
            top = self.stateReg._same()

        if stateFrom is None:
            s = Switch.Default(self, *top)
        else:
            s = Switch.Case(self, stateFrom, *top)
        
        return s
    
    def Default(self, *condAndNextState):
        d = self.Trans(None, *condAndNextState)
        d.stateReg = self.stateReg
        return d

#class While(StmCntx):
#    def __init__(self, cond):
#        self.cnd = _intfToSig(cond)
#    
#    def Do(self, *statements):

    
def _connect(src, dst, exclude, fit):
        
    if isinstance(src, InterfaceBase):
        if isinstance(dst, InterfaceBase):
            return dst._connectTo(src, exclude=exclude, fit=fit)
        src = src._sig
        
    assert not exclude, "this intf. is just a signal"   
    if src is None:
        src = dst._dtype.fromPy(None)
    else:
        src = toHVal(src)
        
    if fit:
        src = fitTo(src, dst)
        
    src = src._dtype.convert(src, dst._dtype)
    
    return [dst._assignFrom(src)]

def connect(src, *destinations, exclude=set(), fit=False):
    """
    Connect src (signals/interfaces/values) to all destinations
    @param exclude: interfaces on any level on src or destinations 
                which should be excluded from connection process
    @param fit: auto fit source width to destination width 
    """
    assignemnts = []
    for dst in destinations:
        assignemnts.extend(_connect(src, dst, exclude, fit))
        
    return assignemnts

def packed(intf, masterDirEqTo=DIRECTION.OUT, exclude=set()):
    """
    Concatenate all signals to one big signal, recursively
    """
    if not intf._interfaces:
        if intf._masterDir == masterDirEqTo:
            return intf._sig
        return None
    
    res = None
    for i in intf._interfaces:
        if i in exclude:
            continue
        
        if i._interfaces:
            if i._masterDir == DIRECTION.IN:
                d = DIRECTION.oposite(masterDirEqTo)
            else:
                d = masterDirEqTo
            s = packed(i, d, exclude=exclude) 
        else:
            if i._masterDir == masterDirEqTo:
                s = i._sig
            else:
                s = None
        
        if s is not None:
            if res is None:
                res = s
            else:
                res = Concat(res, s)
        
    return res

def connectUnpacked(src, dst, exclude=[]):
    """src is packed and it is unpacked and connected to dst"""
    # [TODO] parametrized offsets
    offset = 0
    connections = []
    for i in walkPhysInterfaces(dst):
        if i in exclude:
            continue
        sig = i._sig
        t = sig._dtype
        if t == BIT:
            s = src[hInt(offset)]
            offset += 1
        else:
            w = getWidthExpr(t)
            s = src[(w+offset): offset]
            offset += t.bit_length()
        connections.append(sig._assignFrom(s))
    
    return connections
    
def packedWidth(intf):
    """Sum of all width of interfaces in this interface"""
    if isinstance(intf, type):
        # interface class
        intf = intf()
        intf._loadDeclarations()
    elif isinstance(intf, InterfaceBase) and not hasattr(intf, "_interfaces"):
        # not loaded interface
        intf = deepcopy(intf)
        intf._loadDeclarations()
        
    
    if intf._interfaces:
        w = 0
        for i in intf._interfaces:
            w += packedWidth(i)
        return w
    else:
        t = intf._dtype
        if t == BIT:
            return 1
        return t.bit_length()

def _mkOp(fn): 
    def op(*ops):
        top = None 
        for s in ops:
            if top is None:
                top = s
            else:
                top = fn(top, s)
        return top
    return op

And = _mkOp(lambda top, s: top & s)
Or = _mkOp(lambda top, s: top | s)
Concat = _mkOp(lambda top, s: top._concat(s))

# [TODO] sign correct shift
slr = lambda sig, howMany: vec(0, howMany)._concat(sig[:howMany])
srr = lambda sig, howMany: sig[howMany:]._concat(vec(0, howMany))


c = connect