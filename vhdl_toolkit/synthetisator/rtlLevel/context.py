from python_toolkit.arrayQuery import arr_any, where, distinctBy
from vhdl_toolkit.architecture import Architecture, Component
from vhdl_toolkit.entity import Entity
from vhdl_toolkit.process import HWProcess
from vhdl_toolkit.synthetisator.rtlLevel.codeOp import If, IfContainer
from vhdl_toolkit.synthetisator.rtlLevel.optimalizator import TreeBalancer, \
    expr2cond
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal, walkSigSouces, PortItemFromSignal, PortConnection, \
    SyncSignal, walkUnitInputs, walkSignalsInExpr, OpAnd, \
    discoverSensitivity
from vhdl_toolkit.templates import VHDLTemplates  
from vhdl_toolkit.types import VHDLType
from vhdl_toolkit.synthetisator.param import getParam
from vhdl_toolkit.variables import VHDLGeneric

def renderIfTree(assigments):
    # optimizedSrc = expr_optimize([dp.src])
    # dp.cond = expr_optimize(dp.cond)
    # dp.src = optimizedSrc
    
    for a in assigments:
        if a.cond:
            tb = TreeBalancer(OpAnd)
            cond = expr2cond(tb.balanceExprSet(list(a.cond)))
            ic = IfContainer(cond, [a])
            yield ic
        else:
            yield a


class Context(object):
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
    
    def sig(self, name, width=1, clk=None, syncRst=None, defVal=None):
        """
        generate new signal in context
        @param clk: clk signal, if specified signal is synthetized as SyncSignal
        @param syncRst: reset 
        """
        if name in self.signals:
            raise Exception('signal name "%s" is not unique' % (name))
        
        t = VHDLType()
        width = getParam(width)
        t.width = width
        t.ctx = self.globals

        if clk:
            s = SyncSignal(name, t, defVal)
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
            s = Signal(name, t, defVal)
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
                    if hasattr(node, 'src'):
                        for s in  walkSignalsInExpr(node.src):
                            discoverDatapaths(s)
                    
        for s in where(interfaces, lambda s: s.hasDriver()):  # walk my outputs
            discoverDatapaths(s)
        
    def synthetize(self, interfaces):
        ent = Entity()
        ent.name = self.name
        
        # create generics
        ent.ctx = self.globals
        for k, v in self.globals.items():
            k = k.upper()
            var_type = v.getSigType()
            v.name = k
            g = VHDLGeneric(k, var_type, v)
            ent.generics.append(g)
        
        # create ports
        for s in interfaces:
            s.var_type.ctx = ent.ctx
            ent.port.append(PortItemFromSignal(s))
   
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
       
