from hdl_toolkit.hdlObjects.architecture import Architecture
from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.process import HWProcess
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.serializer.templates import VHDLTemplates  
from hdl_toolkit.synthesizer.assigRenderer import renderIfTree
from hdl_toolkit.synthesizer.codeOps import If
from hdl_toolkit.synthesizer.exceptions import SigLvlConfErr
from hdl_toolkit.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.synthesizer.rtlLevel.memory import RtlSyncSignal
from hdl_toolkit.synthesizer.rtlLevel.optimalizator import removeUnconnectedSignals
from hdl_toolkit.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hdl_toolkit.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hdl_toolkit.synthesizer.rtlLevel.signalUtils.walkers import discoverDriverSignals
from hdl_toolkit.synthesizer.rtlLevel.utils import portItemfromSignal
from python_toolkit.arrayQuery import where, distinctBy, arr_any
from hdl_toolkit.hdlObjects.statements import IfContainer, WaitStm, \
    SwitchContainer


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
    def __init__(self):
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
            
            If(clk._onRisingEdge(), r)
        else:
            if syncRst:
                raise SigLvlConfErr("Signal %s has reset but has no clk" % name)
            s = RtlSignal(self, name, typ, defaultVal=_defVal)
        
        self.signals.add(s)
        
        return s
    
    def cloneSignals(self, signals:list, oldToNewNameFn, cloneAsSync=False):
        buff = []
        for s in signals:
            buff.append(self.sig(oldToNewNameFn(s.name), s.vat_type.width))
        return buff
    
    # def discover(self, interfaces):
    #    """
    #    Discovery process begins on the outputs and tracks back the inputs
    #    """
    #    def discoverDatapaths(signal):
    #        for node in walkSigSouces(signal):
    #            if node in self.startsOfDataPaths:
    #                return 
    #            self.startsOfDataPaths.add(node)
    #            if isinstance(node, PortItem):
    #                if node.unit.discovered is self:
    #                    pass
    #                node.unit.discovered = self
    #                for p in walkUnitInputPorts(node.unit):
    #                    if p.src is not None:  # top unit does not have to be connected
    #                        discoverDatapaths(p.src)
    #                self.subUnits.add(node.unit)
    #            elif isinstance(node, Assignment):
    #                for s in walkSignalsInExpr(node.src):
    #                    discoverDatapaths(s)
    #
    #                for c in node.cond:
    #                    for s in  walkSignalsInExpr(c):
    #                        discoverDatapaths(s)
    #                if node.indexes:
    #                    for i in node.indexes:
    #                        walkSigSouces(i)
    #                
    #            else:
    #                raise NotImplementedError(node)
    #                    
    #        if signal in interfaces:
    #            self.startsOfDataPaths.add(signal)
    #            
    #    for s in where(interfaces, lambda s: signalHasDriver(s)):  # walk my outputs
    #        discoverDatapaths(s)
    #
    def buildProcessesOutOfAssignments(self):
        assigments = list(where(self.startsOfDataPaths,
                                lambda x: isinstance(x, Assignment)
                                )
                          )
        for sig in set(map(lambda x: x.dst, assigments)):
            dps = list(where(assigments,
                             lambda x: x.dst is sig)
                       )
            name = ""
            if not sig.hasGenericName:
                name = sig.name
            # render sequential statements in process
            # (conversion from netlist to statements)
            for stm in renderIfTree(dps):
                p = HWProcess("assig_process_" + name)
                if sig._useNopVal and not isEnclosed(stm):
                    p.statements.append(Assignment(sig._nopVal, sig))
                    
                p.statements.append(stm)
                # [TODO] sensitity list from dps which are covered by stm
                for dp in dps:
                    sensitivity = list(discoverDriverSignals(dp))
                    isEventDependentProc = arr_any(sensitivity, lambda x: x[0])
                    for evDependent, s in sensitivity:
                        # resolve process boundaries and mark them 
                        # and resolve visibility for signals  
                        s.hidden = False
                        
                        if (evDependent and isEventDependentProc) \
                            or not isEventDependentProc:
                            # register sensitivity    
                            p.sensitivityList.add(s)
                            s.simSensitiveProcesses.add(p)
                
            
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
        ent = Entity(name)
        ent._name = name + "_inst"  # instance name

        # create generics
        # ent.ctx = self.globals
        for _, v in self.globals.items():
            ent.generics.append(v)
        
        # create ports
        for s in interfaces:
            pi = portItemfromSignal(s, ent)
            pi.reigsterInternSig(s)
            ent.ports.append(pi)

        removeUnconnectedSignals(self)
        # self.discover(interfaces)
        
        arch = Architecture(ent)
        for p in self.buildProcessesOutOfAssignments():
            arch.processes.append(p)
            

        # add signals, variables etc. in architecture
        for s in self.signals:
            if s.endpoints or s.drivers or s.simSensitiveProcesses:  # if is used
                if s not in interfaces and not s.hidden:
                    arch.variables.append(s)
        
        # instanciate subUnits in architecture
        for u in self.subUnits:  
            arch.componentInstances.append(u) 
        
        # add components in architecture    
        for su in distinctBy(self.subUnits, lambda x: x.name):
            arch.components.append(su)
        
        self.synthesised = True
        
        # [TODO] real references based on real ent/arch objects 
        return [ VHDLTemplates.basic_include, ent, arch]
       
