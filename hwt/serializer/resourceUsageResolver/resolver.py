from typing import List

from hwt.hdl.architecture import Architecture
from hwt.hdl.assignment import Assignment
from hwt.hdl.entity import Entity
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.process import HWProcess
from hwt.hdl.statements import IfContainer, SwitchContainer
from hwt.hdl.types.array import HArray
from hwt.hdl.value import Value
from hwt.serializer.generic.serializer import GenericSerializer
from hwt.serializer.resourceUsageResolver.resourceTypes import Unconnected, \
    ResourceMUX, ResourceLatch, ResourceLatchWithMux
from hwt.serializer.resourceUsageResolver.utils import ResourceContext, \
    updateGuesFromAssignment, resourceTransitions_override, mergeGues, \
    operatorsWithoutResource
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class ResourceUsageResolver(GenericSerializer):
    """
    Serializer which does not products any output just collect informations
    about used resources
    
    :attention: Use instance of ResourceUsageResolver instead of class
    """
    _keywords_dict = {}
    def __init__(self):
        self.context = ResourceContext(None)

    @classmethod
    def HWProcess(cls, proc: HWProcess, ctx: ResourceContext):
        gues = cls.statementList(proc.statements, proc.outputs, ctx)
        for sig, resGues in gues.items():
            ctx.register(sig, resGues)

    @classmethod
    def statementList(cls, statements, dstSignals, ctx: ResourceContext):
        gues = {}
        guesOfChildren = []
        # resolve 
        olnlyAssignmets = True
        for stm in statements:
            if isinstance(stm, Assignment):
                updateGuesFromAssignment(gues, stm)
                if isinstance(stm.src, RtlSignal):
                    cls.Signal(stm.src, ctx)
            else:
                olnlyAssignmets = False
                fn = getattr(cls, stm.__class__.__name__)
                g = fn(stm, dstSignals, ctx)
                guesOfChildren.append(g)
        
        for g in guesOfChildren:
            for sig, childGues in g.items():
                try:
                    current = gues[sig]
                except KeyError:
                    current = Unconnected

                nextGues = resourceTransitions_override[(current, childGues)]
                gues[sig] = nextGues

        # mark signals which were not connected as unconnected
        if olnlyAssignmets:
            for sig in dstSignals:
                if sig not in gues.keys():
                    gues[sig] = Unconnected

        return gues
    
    @classmethod
    def condition(cls, condition:List[RtlSignal], ctx: ResourceContext):
        for signal in condition:
            cls.Signal(signal, ctx)
    
    @classmethod
    def IfContainer(cls, ifc: IfContainer, dstSignals, ctx: ResourceContext):
        cls.condition(ifc.cond, ctx)
        
        ifTrue = cls.statementList(ifc.ifTrue, dstSignals, ctx)
        
        for elifCond, elifStm in ifc.elIfs:
            cls.condition(elifCond, ctx)
            elifGues = cls.statementList(elifStm, dstSignals, ctx)
            mergeGues(ifTrue, elifGues)
            
        if ifc.ifFalse:
            ifFalse = cls.statementList(ifc.ifFalse, dstSignals, ctx)
            mergeGues(ifTrue, ifFalse)
            
        return ifTrue

    @classmethod
    def SwitchContainer(cls, swc: SwitchContainer, dstSignals, ctx: ResourceContext):
        isEnclosed = swc.default or (1 << len(swc.cases))
        gues = None
        for k, c in swc.cases:
            g = cls.statementList(c, dstSignals, ctx)
            if gues is None:
                gues = g
            else:
                mergeGues(gues, g)
        
        if swc.default:
            g = cls.statementList(swc.default, dstSignals, ctx)
            if gues is None:
                gues = g
            else:
                mergeGues(gues, g)
        
        if not isEnclosed:
            # convert all multiplexers or assignments to latches
            update = {}
            for k, v in gues.items():
                if v is Assignment:
                    update[k] = ResourceLatch  
                elif v is ResourceMUX:
                    update[k] = ResourceLatchWithMux
            gues.update(update)
            
        return gues
            
    @classmethod
    def Signal(cls, signal: RtlSignal, ctx: ResourceContext):
        """
        Resolve resources for signal by walking it's drivers
        """
        # skip constants because they does not consume any resources
        # directly
        if not signal._const and signal not in ctx.seen:
            ctx.seen.add(signal)
            # walk drivers to find rest of resources in expression
            for driver in signal.drivers:
                if isinstance(driver, Operator):
                    op = driver.operator
                    if op is AllOps.INDEX:
                        # index can be MUX/memory/static bit select
                        i = driver.operands[1] 
                        if isinstance(i, Value) or i._const:
                            # bit selecting operator
                            pass
                        else:
                            # mux or read ram port
                            inputsSig = driver.operands[0]
                            if isinstance(inputsSig._dtype, HArray):
                                # this indexing is read port of some RAM/ROM
                                ctx.discoveredRamSignals.add(inputsSig)
                            else:
                                # this indexing is MUX
                                width = driver.result._dtype.bit_length()
                                inputs = inputsSig._dtype.bit_length() // width 
                                ctx.registerMUX_known(width, inputs)
                    # skip conversions/clk ops etc. which does not consume
                    # resources directly
                    elif op not in operatorsWithoutResource:
                        
                        if op is AllOps.TERNARY:
                            # ternary can be to Bits(1) conversion
                            try:
                                a = bool(driver.operands[1])
                                b = bool(driver.operands[2])
                            except ValueError:
                                a = False
                                b = False

                            if a and not b:
                                # this is just to bit conversion if cond: 1 else 0
                                pass
                            else:
                                # this is multiplexer
                                width = signal._dtype.bit_length()
                                inputsCnt = 2
                                ctx.registerMUX_known(width, inputsCnt)

                        else:
                            doRegister = True
                            # check to bool conversion
                            if op is AllOps.EQ and driver.operands[0]._dtype.bit_length() == 1:
                                try:
                                    a = bool(driver.operands[1])
                                    # if this is just to bool conversion skip it
                                    doRegister = not a
                                except ValueError:
                                    doRegister = True

                            if doRegister:
                                ctx.registerOperator(driver)

                    # collect resources for other operators as well
                    for oper in driver.operands:
                        if isinstance(oper, RtlSignal):
                            cls.Signal(oper, ctx)

                elif isinstance(driver, Assignment):
                    # processed by HWProcess
                    pass
                else:
                    raise NotImplementedError(driver)

    @classmethod
    def Entity(cls, ent: Entity, ctx: ResourceContext):
        """
        Entity is just header, we do not need to inspect it for resources
        """
        return

    def getBaseContext(self):
        """
        Return context for collecting of resource informatins
        prepared on this instance
        """
        return self.context
    
    @classmethod
    def Architecture(cls, arch: Architecture, ctx: ResourceContext):
        for c in arch.componentInstances:
            raise NotImplementedError()

        for proc in arch.processes:
            cls.HWProcess(proc, ctx)
        
        ctx.finalize()

    def report(self):
        return self.context.resources
        
