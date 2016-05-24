from python_toolkit.arrayQuery import where, distinctBy

from hdl_toolkit.hdlObjects.architecture import Architecture
from hdl_toolkit.hdlObjects.component import  Component
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.hdlObjects.process import HWProcess
from hdl_toolkit.hdlObjects.portConnection import PortConnection
from hdl_toolkit.hdlObjects.typeDefs import BIT
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.assignment import Assignment

from hdl_toolkit.synthetisator.rtlLevel.signal import Signal, SyncSignal
from hdl_toolkit.synthetisator.rtlLevel.codeOp import If
from hdl_toolkit.synthetisator.rtlLevel.utils import portItemfromSignal
from hdl_toolkit.synthetisator.rtlLevel.signalWalkers import  walkUnitInputs, walkSignalsInExpr, \
    discoverSensitivity, walkSigSouces, signalHasDriver
from hdl_toolkit.synthetisator.templates import VHDLTemplates  
from hdl_toolkit.synthetisator.exceptions import SigLvlConfErr

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
            raise Exception('signal name "%s" is not unique' % (name))
        if defVal is not None and not isinstance(defVal, Value):
            defVal = Value.fromPyVal(defVal, typ)

        if clk is not None:
            s = SyncSignal(name, typ, defVal)
            if syncRst is not None and defVal is None:
                raise Exception("Probably forgotten default value on sync signal %s", name)
            if syncRst is not None:
                r = If(syncRst._isOn(),
                            [Signal._assignFrom(s, defVal)] ,
                            [Signal._assignFrom(s, s.next)])
            else:
                r = [Signal._assignFrom(s, s.next)]
            
            If(clk._onRisingEdge(), r)
        else:
            if syncRst:
                raise SigLvlConfErr("Signal %s has reset but has no clk" % name)
            s = Signal(name, typ, defaultVal=defVal)
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
                    assert(isinstance(node.cond, set))
                    for c in node.cond:
                        for s in  walkSignalsInExpr(c):
                            discoverDatapaths(s)
                else:
                    raise NotImplementedError()
                        
            if signal in interfaces:
                self.startsOfDataPaths.add(signal)
                
        for s in where(interfaces, lambda s: signalHasDriver(s)):  # walk my outputs
            discoverDatapaths(s)
    
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
        # for s in where(arch.statements, lambda x: isinstance(x, PortConnection)):  # find subUnits
        #    self.subUnits.add(self.unit)
        assigments = list(where(self.startsOfDataPaths, lambda x: isinstance(x, Assignment)))
        for sig in set(map(lambda x:x.dst, assigments)):
            dps = list(where(assigments, lambda x: x.dst == sig))
            p = HWProcess("assig_process_" + sig.name)
            for dp in dps:
                p.sensitivityList.update(map(lambda x: x.name, discoverSensitivity(dp)))
            p.bodyBuff.extend(dps) 
            arch.processes.append(p)
            
            # [TODO] support for dynamically created signals
            #if sig.name not in self.signals:
            #    self.signals[sig.name] = sig

        # add signals, variables etc. in architecture
        for _, s in self.signals.items():
            if s not in interfaces:
                # [TODO] if has driver
                arch.variables.append(s)
                if isinstance(s, SyncSignal):
                    arch.variables.append(s.next)
        
        # instanciate subUnits in architecture
        for u in self.subUnits:  
            arch.componentInstances.append(u.asVHDLComponentInstance(u._name + "_inst")) 
        
        # add components in architecture    
        for su in distinctBy(self.subUnits, lambda x: x.name):
            c = Component(su)
            arch.components.append(c)
        
        # [TODO] real references based on real ent/arch objects 
        return [ VHDLTemplates.basic_include, ent, arch]
       
