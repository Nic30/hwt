from python_toolkit.arrayQuery import arr_any, where, distinctBy
from vhdl_toolkit.types import VHDLType, VHDLBoolean
from vhdl_toolkit.synthetisator.signal import Signal, walkSigSouces, PortItemFromSignal, PortConnection, \
    SynSignal, walkUnitInputs, walkSignalsInExpr, exp__str__, OpAnd, \
    discoverSensitivity
from vhdl_toolkit.entity import Entity
from vhdl_toolkit.architecture import Architecture, Component
from vhdl_toolkit.variables import PortItem
from vhdl_toolkit.templates import VHDLTemplates  
from vhdl_toolkit.process import HWProcess
from vhdl_toolkit.synthetisator.codeOp import If, IfContainer
from vhdl_toolkit.synthetisator.optimalizator import TreeBalancer, expr_optimize, \
    expr2cond


def renderIfTree(assigments):
    # optimizedSrc = expr_optimize([dp.src])
    # dp.cond = expr_optimize(dp.cond)
    # dp.src = optimizedSrc
    
    for a in assigments:
        if a.cond:
            cond = expr2cond(a.cond)
            ic = IfContainer(cond, a)
            yield ic
        else:
            yield a


class Context(object):
    def __init__(self, name, debug=True):
        self.signals = []
        self.name = name
        self.debug = debug
    
    def sig(self, name, width, clk=None, syncRst=None, defVal=None):
        if self.debug and arr_any(self.signals, lambda x: x.name == name):
            raise Exception('signal name "%s" is not unique' % (name))
        
        t = VHDLType()
        t.width = width
        
        if width > 1:
            t.str = 'STD_LOGIC_VECTOR(%d DOWNTO 0)' % (width - 1)
        elif width == 1:
            t.str = 'STD_LOGIC'
        else:
            raise Exception("Invalid size for signal %s" % (name))
        if clk:
            s = SynSignal(name, t, defVal)
            if syncRst is not None and defVal is None:
                raise Exception("Probably forgotten default value on sync signal %s", name)
            if syncRst is not None and defVal is not None:
                r = If(syncRst.opIsOn(), [Signal.assign(s, defVal)] ,
                                        [Signal.assign(s, s.next)])
            else:
                r = [Signal.assign(s, s.next)]
            
            If(clk.opOnRisigEdge(), r)
        else:
            s = Signal(name, t, defVal)
        self.signals.append(s)
        return s
    
    def cloneSignals(self, signals, oldToNewNameFn, cloneAsSync=False):
        buff = []
        for s in signals:
            buff.append(self.sig(oldToNewNameFn(s.name), s.vat_type.width))
        return buff
        
    def synthetize(self, name, interfaces):
        ent = Entity()
        ent.name = name
        
        for s in interfaces:
            ent.port.append(PortItemFromSignal(s))

        arch = Architecture(ent)
        startsOfDataPaths = set()
        subUnits = set()
        def discoverDatapaths(signal):
                for node in walkSigSouces(signal):  
                    if node in startsOfDataPaths:
                        return 
                    # print(str(node.__class__), str(node))
                    if isinstance(node, PortConnection) and not node.unit.discovered:
                        node.unit.discovered = True
                        for s in  walkUnitInputs(node.unit):
                            discoverDatapaths(s)
                        subUnits.add(node.unit)
                    startsOfDataPaths.add(node)
                    if hasattr(node, 'src'):
                        for s in  walkSignalsInExpr(node.src):
                            # print("discovering signal %s" % (str(s)))
                            discoverDatapaths(s)

                            
                    
        for s in where(ent.port, lambda x: x.direction == x.typeOut):  # walk my outputs
            discoverDatapaths(s.sig)
            
        for s in where(arch.statements, lambda x: isinstance(x, PortConnection)):  # found subUnits
            subUnits.add(self.unit)
        assigments = list(where(startsOfDataPaths, lambda x: hasattr(x, 'dst')))
        for sig in set(map(lambda x:x.dst, assigments)):
            dps = list(where(assigments, lambda x: x.dst == sig))
            p = HWProcess("assig_process_" + sig.name)
            for dp in dps:
                p.sensitivityList.update(map(lambda x: x.name, discoverSensitivity(dp)))
            p.bodyBuff.extend(renderIfTree(dps)) 
            arch.processes.append(p)
        # arch.statements = list(where(arch.statements, lambda x: not isinstance(x, PortConnection))) 
        
        for s in self.signals:
            if s not in interfaces:
                arch.variables.append(s)
                if isinstance(s, SynSignal):
                    arch.variables.append(s.next)
        
        for u in subUnits:  # instanciate subUnits
            arch.componentInstances.append(u.asVHDLComponentInstance()) 
            
        for su in distinctBy(subUnits, lambda x: x.name):
            c = Component(su)
            arch.components.append(c)
         
        return [ VHDLTemplates.basic_include, ent, arch]
       
