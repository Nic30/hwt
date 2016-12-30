from hwt.hdlObjects.architecture import Architecture
from hwt.hdlObjects.assignment import Assignment
from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.process import HWProcess
from hwt.hdlObjects.statements import IfContainer, WaitStm, \
    SwitchContainer
from hwt.hdlObjects.types.defs import BIT
from hwt.hdlObjects.value import Value
from hwt.synthesizer.assigRenderer import renderIfTree
from hwt.code import If
from hwt.synthesizer.exceptions import SigLvlConfErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.memory import RtlSyncSignal
from hwt.synthesizer.rtlLevel.optimalizator import removeUnconnectedSignals
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.synthesizer.rtlLevel.signalUtils.walkers import discoverSensitivity
from hwt.synthesizer.rtlLevel.utils import portItemfromSignal
from hwt.pyUtils.arrayQuery import where, distinctBy, groupedby


def isSignalHiddenInExpr(sig):
    """Some signals are just only connections in expression they done need to be rendered because
    they are hidden inside expression for example sig. from a+b in a+b+c"""
    if isinstance(sig, Value):
        return True
    try:
        d = sig.singleDriver()
        if isinstance(d, Operator):
            return True
    except MultipleDriversExc:
        pass
        
    return False

def _isEnclosed(objList):
    if not objList:
        return False
    for o in objList:
        if not isEnclosed(o):
            return False
    return True
    
def isEnclosed(obj):
    """
    Check if statement has any not used branch
    """
    if isinstance(obj, (Assignment, WaitStm)):
        return True
    elif isinstance(obj, IfContainer):
        for ol in [obj.ifTrue, obj.ifFalse]:
            if not _isEnclosed(ol):
                return False
        for _, ol in obj.elIfs:
            if not _isEnclosed(ol):
                return False
                
        return True 
    elif isinstance(obj, SwitchContainer):
        allCasesCovered = True
        for cond, ol in obj.cases:
            if cond is None:
                allCasesCovered = True
            if not _isEnclosed(ol):
                return False
            
        return allCasesCovered
    else:
        raise NotImplementedError(obj)


class RtlNetlist():
    """
    Container for signals and units
    @ivar signals: dict of all signals in context
    @ivar startsOfDataPaths:  is set of nodes where datapaths starts
    @ivar subUnits:           is set of all units in this context 
    """
    def __init__(self, parentForDebug=None):
        self.parentForDebug = parentForDebug
        self.globals = {}
        self.signals = set()
        self.startsOfDataPaths = set()
        self.subUnits = set()
        self.synthesised = False

    
    def sig(self, name, typ=BIT, clk=None, syncRst=None, defVal=None):
        """
        generate new signal in context
        @param clk: clk signal, if specified signal is synthesized as SyncSignal
        @param syncRst: reset 
        """
        if not isinstance(defVal, (Value, RtlSignal, InterfaceBase)):
            if isinstance(defVal, (InterfaceBase)):
                _defVal = defVal._sig
            else:    
                _defVal = typ.fromPy(defVal)
        else:
            _defVal = defVal._convert(typ)


        if clk is not None:
            s = RtlSyncSignal(self, name, typ, _defVal)
            if syncRst is not None and defVal is None:
                raise Exception("Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                        [RtlSignal.__pow__(s, _defVal)]
                    ).Else(
                        [RtlSignal.__pow__(s, s.next)]
                    )
            else:
                r = [RtlSignal.__pow__(s, s.next)]
            
            If(clk._onRisingEdge(),
               r)
        else:
            if syncRst:
                raise SigLvlConfErr("Signal %s has reset but has no clk" % name)
            s = RtlSignal(self, name, typ, defaultVal=_defVal)
        
        self.signals.add(s)
        
        return s
   
    def buildProcessesOutOfAssignments(self):
        """
        Render conditional assignments to statements and wrap them with process statement
        """
        assigments = where(self.startsOfDataPaths,
                            lambda x: isinstance(x, Assignment)
                          )
        for sig, dps in groupedby(assigments, lambda x: x.dst):
            dps = list(dps)
            name = ""
            if not sig.hasGenericName:
                name = sig.name
            sig.hidden = False
            
            haveNotIndexes = True
            for dp in dps:
                haveNotIndexes = haveNotIndexes and not dp.indexes
            
            # render sequential statements in process
            # (conversion from netlist to statements)
            hasCombDriver = False
            for stm in renderIfTree(dps):
                
                p = HWProcess("assig_process_" + name)
                if sig._useNopVal and not isEnclosed(stm):
                    n = sig._nopVal
                    p.statements.append(Assignment(n, sig))
                    if isinstance(n, RtlSignal):
                        p.sensitivityList.add(n)
                    
                p.statements.append(stm)

                sensitivity = discoverSensitivity(stm)
                p.sensitivityList.update(sensitivity)

                isEventDependent = False
                for s in p.sensitivityList:
                    if isinstance(s, Operator):
                        # event operator
                        s.ops[0].hidden = False
                        isEventDependent = True
                    else:
                        s.hidden = False

                if hasCombDriver and not isEventDependent and haveNotIndexes:
                    raise MultipleDriversExc("Signal %s has multiple combinational drivers" % name)
                hasCombDriver = hasCombDriver or not isEventDependent
                
                yield p

    def mergeWith(self, other):
        """
        Merge two instances into this
        @attention: "others" becomes invalid because all signals etc. will be transferred into this 
        """
        assert not other.synthesised
        self.globals.update(other.globals)
        self.signals.update(other.signals)
        self.startsOfDataPaths.update(other.startsOfDataPaths)
        self.subUnits.update(other.subUnits)
        
        for s in other.signals:
            s.ctx = self
        

    def synthesize(self, name, interfaces):
        """
        Build Entity and architecture out of netlist representation
        """
        
        ent = Entity(name)
        ent._name = name + "_inst"  # instance name

        # create generics
        for _, v in self.globals.items():
            ent.generics.append(v)
        
        # create ports
        for s in interfaces:
            pi = portItemfromSignal(s, ent)
            pi.reigsterInternSig(s)
            ent.ports.append(pi)

        removeUnconnectedSignals(self)
        
        arch = Architecture(ent)
        for p in self.buildProcessesOutOfAssignments():
            arch.processes.append(p)
            

        # add signals, variables etc. in architecture
        for s in self.signals:
            if s not in interfaces and not s.hidden:
                arch.variables.append(s)
        
        # instanciate subUnits in architecture
        for u in self.subUnits:  
            arch.componentInstances.append(u) 
        
        # add components in architecture    
        for su in distinctBy(self.subUnits, lambda x: x.name):
            arch.components.append(su)
        
        self.synthesised = True
        
        return [ent, arch]
       
