from python_toolkit.arrayQuery import where, distinctBy
from vhdl_toolkit.hdlObjects.architecture import Architecture, Component
from vhdl_toolkit.hdlObjects.variables import VHDLGeneric
from vhdl_toolkit.hdlObjects.entity import Entity
from vhdl_toolkit.hdlObjects.process import HWProcess
from vhdl_toolkit.synthetisator.rtlLevel.codeOp import If, IfContainer
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal, SyncSignal
from vhdl_toolkit.hdlObjects.portConnection import PortConnection
from vhdl_toolkit.synthetisator.rtlLevel.utils import portItemfromSignal
from vhdl_toolkit.synthetisator.rtlLevel.signalWalkers import  walkUnitInputs, walkSignalsInExpr, \
    discoverSensitivity, walkSigSouces, signalHasDriver
from vhdl_toolkit.templates import VHDLTemplates  
from vhdl_toolkit.hdlObjects.typeDefs import BIT
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.assignment import Assignment

def renderIfTree(assigments):
    # optimizedSrc = expr_optimize([dp.src])
    # dp.cond = expr_optimize(dp.cond)
    # dp.src = optimizedSrc
    
    for a in assigments:
        if a.cond:
            ic = IfContainer(a.cond, [a])
            yield ic
        else:
            yield a


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

        if clk:
            s = SyncSignal(name, typ, defVal)
            if syncRst is not None and defVal is None:
                raise Exception("Probably forgotten default value on sync signal %s", name)
            if syncRst is not None and defVal is not None:
                r = If(syncRst.opIsOn(), [Signal.assignFrom(s, defVal)] ,
                                        [Signal.assignFrom(s, s.next)])
            else:
                r = [Signal.assignFrom(s, s.next)]
            
            If(clk.opOnRisigEdge(), r)
        else:
            if syncRst:
                raise Exception()
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
                    if isinstance(node, PortConnection) and not node.unit.discovered:
                        node.unit.discovered = True
                        for s in  walkUnitInputs(node.unit):
                            discoverDatapaths(s)
                        self.subUnits.add(node.unit)
                    self.startsOfDataPaths.add(node)
                    if isinstance(node, Assignment):
                        for s in walkSignalsInExpr(node.src):
                            discoverDatapaths(s)
                    
        for s in where(interfaces, lambda s: signalHasDriver(s)):  # walk my outputs
            discoverDatapaths(s)
    
    def synthetize(self, interfaces):
        ent = Entity()
        ent.name = self.name
        
        # create generics
        ent.ctx = self.globals
        for k, v in self.globals.items():
            k = k.upper()
            #v.name = k
            g = VHDLGeneric(k, v.dtype, v)
            ent.generics.append(g)
        
        # create ports
        for s in interfaces:
            #s.dtype.ctx = ent.ctx
            ent.ports.append(portItemfromSignal(s))
   
        self.discover(interfaces)
        
        arch = Architecture(ent)
        # for s in where(arch.statements, lambda x: isinstance(x, PortConnection)):  # find subUnits
        #    self.subUnits.add(self.unit)
        assigments = list(where(self.startsOfDataPaths, lambda x: hasattr(x, 'dst')))
        for sig in set(map(lambda x:x.dst, assigments)):
            dps = list(where(assigments, lambda x: x.dst == sig))
            p = HWProcess("assig_process_" + sig.name)
            for dp in dps:
                p.sensitivityList.update(map(lambda x: x.name, discoverSensitivity(dp)))
            p.bodyBuff.extend(renderIfTree(dps)) 
            arch.processes.append(p)

        # add signals, variables etc. in architecture
        for _, s in self.signals.items():
            if s not in interfaces:
                # [TODO] if has driver
                arch.variables.append(s)
                if isinstance(s, SyncSignal):
                    arch.variables.append(s.next)
        
        # instanciate subUnits in architecture
        for u in self.subUnits:  
            arch.componentInstances.append(u.asVHDLComponentInstance()) 
        
        # add components in architecture    
        for su in distinctBy(self.subUnits, lambda x: x.name):
            c = Component(su)
            arch.components.append(c)
         
        return [ VHDLTemplates.basic_include, ent, arch]
       
