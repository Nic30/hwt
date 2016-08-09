from python_toolkit.arrayQuery import where, distinctBy, arr_any

from hdl_toolkit.hdlObjects.architecture import Architecture
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.hdlObjects.process import HWProcess
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.assignment import Assignment

from hdl_toolkit.synthetisator.rtlLevel.rtlSignal import RtlSignal
from hdl_toolkit.synthetisator.codeOps import If
from hdl_toolkit.synthetisator.rtlLevel.utils import portItemfromSignal
from hdl_toolkit.synthetisator.rtlLevel.signalUtils.walkers import walkUnitInputPorts, walkSignalsInExpr, \
    discoverDriverSignals, walkSigSouces, signalHasDriver
from hdl_toolkit.serializer.templates import VHDLTemplates  
from hdl_toolkit.synthetisator.exceptions import SigLvlConfErr
from hdl_toolkit.synthetisator.assigRenderer import renderIfTree
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.synthetisator.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hdl_toolkit.synthetisator.rtlLevel.memory import RtlSyncSignal
from hdl_toolkit.hdlObjects.portItem import PortItem
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase

def isUnnamedIndex(sig):
    return (hasattr(sig, "origin") and 
            sig.origin.operator == AllOps.INDEX and
            sig.hasGenericName)
        
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
        
    return isUnnamedIndex(sig)

class RtlNetlist():
    """
    Container for signals and units
    @ivar signals: dict of all signals in context
    @ivar startsOfDataPaths: is created by discover(interfaces), is set of nodes where datapaths starts
    @ivar subUnits:           --------------||---------------------------- all units in this context 
    """
    def __init__(self, name, globalNames:dict=None):
        """
        @param name: name of context is synthesized as entity name
        @param globalNames: dictionary of parameters is synthesized as entity generics  
        """
        if not globalNames:
            self.globals = {}
        else:
            self.globals = globalNames
        self.signals = {}
        self.name = name

    
    def sig(self, name, typ=BIT, clk=None, syncRst=None, defVal=None):
        """
        generate new signal in context
        @param clk: clk signal, if specified signal is synthesized as SyncSignal
        @param syncRst: reset 
        """

        if name in self.signals:
            raise Exception('%s:signal name "%s" is not unique' % (self.name, name))
        if not isinstance(defVal, (Value, RtlSignal, InterfaceBase)):
            if isinstance(defVal, (InterfaceBase)):
                _defVal = defVal._sig
            else:    
                _defVal = typ.fromPy(defVal)
        else:
            _defVal = defVal._convert(typ)


        if clk is not None:
            s = RtlSyncSignal(name, typ, _defVal)
            if syncRst is not None and defVal is None:
                raise Exception("Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                        [RtlSignal._assignFrom(s, _defVal)]
                    ).Else(
                        [RtlSignal._assignFrom(s, s.next)]
                    )
            else:
                r = [RtlSignal._assignFrom(s, s.next)]
            
            If(clk._onRisingEdge(), r)
        else:
            if syncRst:
                raise SigLvlConfErr("Signal %s has reset but has no clk" % name)
            s = RtlSignal(name, typ, defaultVal=_defVal)
        self.signals[name] = s
        return s
    
    def cloneSignals(self, signals:list, oldToNewNameFn, cloneAsSync=False):
        buff = []
        for s in signals:
            buff.append(self.sig(oldToNewNameFn(s.name), s.vat_type.width))
        return buff
    
    def discover(self, interfaces):
        """
        Discovery process begins on the outputs and tracks back the inputs
        """
        self.startsOfDataPaths = set()
        self.subUnits = set()
        
        def discoverDatapaths(signal):
            for node in walkSigSouces(signal):
                if node in self.startsOfDataPaths:
                    return 
                self.startsOfDataPaths.add(node)
                if isinstance(node, PortItem):
                    if node.unit.discovered is self:
                        pass
                    node.unit.discovered = self
                    for p in walkUnitInputPorts(node.unit):
                        if p.src is not None:  # top unit does not have to be connected
                            discoverDatapaths(p.src)
                    self.subUnits.add(node.unit)
                elif isinstance(node, Assignment):
                    for s in walkSignalsInExpr(node.src):
                        discoverDatapaths(s)
                    assert isinstance(node.cond, set)
                    for c in node.cond:
                        for s in  walkSignalsInExpr(c):
                            discoverDatapaths(s)
                else:
                    raise NotImplementedError()
                        
            if signal in interfaces:
                self.startsOfDataPaths.add(signal)
                
        for s in where(interfaces, lambda s: signalHasDriver(s)):  # walk my outputs
            discoverDatapaths(s)
    
    def buildProcessesOutOfAssignments(self):
        assigments = list(where(self.startsOfDataPaths,
                                lambda x: isinstance(x, Assignment)
                                )
                          )
        for sig in set(map(lambda x:x.dst, assigments)):
            dps = list(where(assigments,
                             lambda x: x.dst == sig)
                       )
            p = HWProcess("assig_process_" + sig.name)
            # render sequential statements in process
            # (conversion from netlist to statements)
            for stm in renderIfTree(dps):
                p.statements.append(stm) 

            for dp in dps:
                sensitivity = list(discoverDriverSignals(dp))
                isEventDependentProc = arr_any(sensitivity, lambda x: x[0])
                for evDependent, s in sensitivity:
                    # resolve process boundaries and mark them 
                    # and resolve visibility for signals  
                    s.hidden = False
                    if s.name not in self.signals:
                        self.signals[s.name] = s
                    
                    if (evDependent and isEventDependentProc) \
                        or not isEventDependentProc:
                        # register sensitivity    
                        p.sensitivityList.add(s)
                        s.simSensitiveProcesses.add(p)
            
            
            yield p

    def synthesize(self, interfaces):
        ent = Entity(self.name)
        ent._name = self.name + "_inst"  # instance name
        

        # create generics
        ent.ctx = self.globals
        for _, v in self.globals.items():
            ent.generics.append(v)
        
        # create ports
        for s in interfaces:
            pi = portItemfromSignal(s, ent)
            pi.reigsterInternSig(s)
            ent.ports.append(pi)

        self.discover(interfaces)
        
        arch = Architecture(ent)
        for p in self.buildProcessesOutOfAssignments():
            arch.processes.append(p)
            

        # add signals, variables etc. in architecture
        for _, s in self.signals.items():
            if s.endpoints or s.drivers or s.simSensitiveProcesses: # if is used
                if s not in interfaces:
                    arch.variables.append(s)
        
        # instanciate subUnits in architecture
        for u in self.subUnits:  
            arch.componentInstances.append(u) 
        
        # add components in architecture    
        for su in distinctBy(self.subUnits, lambda x: x.name):
            arch.components.append(su)
        
        # [TODO] real references based on real ent/arch objects 
        return [ VHDLTemplates.basic_include, ent, arch]
       
