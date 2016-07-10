from python_toolkit.arrayQuery import where, distinctBy

from hdl_toolkit.hdlObjects.architecture import Architecture
from hdl_toolkit.hdlObjects.component import  Component
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.hdlObjects.process import HWProcess
from hdl_toolkit.hdlObjects.portConnection import PortConnection
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.assignment import Assignment

from hdl_toolkit.synthetisator.rtlLevel.signal import RtlSignal
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.synthetisator.rtlLevel.utils import portItemfromSignal
from hdl_toolkit.synthetisator.rtlLevel.signal.walkers import  walkUnitInputs, walkSignalsInExpr, \
    discoverSensitivity, walkSigSouces, signalHasDriver
from hdl_toolkit.synthetisator.templates import VHDLTemplates  
from hdl_toolkit.synthetisator.exceptions import SigLvlConfErr
from hdl_toolkit.synthetisator.assigRenderer import renderIfTree
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.synthetisator.rtlLevel.signal.exceptions import MultipleDriversExc
from hdl_toolkit.synthetisator.rtlLevel.memory import RtlSyncSignal

def isUnnamedIndex(sig):
    return (hasattr(sig, "origin") and 
            sig.origin.operator == AllOps.INDEX and
            sig.hasGenericName)
        
def isSignalHiddenInExpr( sig):
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

# [TODO] rename to RtlNetlist
class Context():
    """
    Container for signals and units
    @ivar signals: dict of all signals in context
    @ivar startsOfDataPaths: is created by discover(interfaces), is set of nodes where datapaths starts
    @ivar subUnits:           --------------||---------------------------- all units in this context 
    """
    def __init__(self, name, globalNames:dict=None):
        """
        @param name: name of context is synthetized as entity name
        @param globalNames: dictionary of parameters is synthetized as entity generics  
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
        @param clk: clk signal, if specified signal is synthetized as SyncSignal
        @param syncRst: reset 
        """

        if name in self.signals:
            raise Exception('%s:signal name "%s" is not unique' % (self.name, name))
        _defVal = typ.fromPy(defVal)


        if clk is not None:
            s = RtlSyncSignal(name, typ, _defVal)
            if syncRst is not None and defVal is None:
                raise Exception("Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                            [RtlSignal._assignFrom(s, _defVal)] ,
                            [RtlSignal._assignFrom(s, s.next)])
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
        self.startsOfDataPaths = set()
        self.subUnits = set()
        def discoverDatapaths(signal):
            for node in walkSigSouces(signal):
                if node in self.startsOfDataPaths:
                    return 
                self.startsOfDataPaths.add(node)
                if isinstance(node, PortConnection) and not node.unit.discovered:
                    node.unit.discovered = True
                    for s in walkUnitInputs(node.unit):
                        discoverDatapaths(s)
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
            for dp in dps:
                for s in discoverSensitivity(dp):
                    # resolve process boundaries and mark them 
                    # and resolve visibility for signals  
                    s.hidden = False
                    if s.name not in self.signals:
                        self.signals[s.name] = s
                    
                    # register sensitivity    
                    p.sensitivityList.add(s)
                    s.simSensitiveProcesses.add(p)
            
            # render sequential statements in process
            # (conversion from netlist to statements)
            for stm in renderIfTree(dps):
                p.statements.append(stm) 
            
            yield p

    def synthetize(self, interfaces):
        ent = Entity()
        ent.name = self.name

        # create generics
        ent.ctx = self.globals
        for _, v in self.globals.items():
            ent.generics.append(v)
        
        # create ports
        for s in interfaces:
            ent.ports.append(portItemfromSignal(s))
   
        self.discover(interfaces)
        
        arch = Architecture(ent)
        for p in self.buildProcessesOutOfAssignments():
            arch.processes.append(p)
            

        # add signals, variables etc. in architecture
        for _, s in self.signals.items():
            if s not in interfaces:
                # [TODO] if has driver
                arch.variables.append(s)
        
        # instanciate subUnits in architecture
        for u in self.subUnits:  
            arch.componentInstances.append(u.asVHDLComponentInstance(u._name + "_inst")) 
        
        # add components in architecture    
        for su in distinctBy(self.subUnits, lambda x: x.name):
            c = Component(su)
            arch.components.append(c)
        
        # [TODO] real references based on real ent/arch objects 
        return [ VHDLTemplates.basic_include, ent, arch]
       
