import sys

from hdl_toolkit.hdlObjects.architecture import Architecture
from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.hdlObjects.process import HWProcess
from hdl_toolkit.hdlObjects.statements import WaitStm
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.boolean import Boolean
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.serializer.vhdlSerializer import VhdlSerializer
from hdl_toolkit.simulator.hdlSimConfig import HdlSimConfig
from hdl_toolkit.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces
from hdl_toolkit.synthesizer.rtlLevel.netlist import RtlNetlist
from hdl_toolkit.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hdl_toolkit.synthesizer.codeOps import connect


def makeTestbenchTemplate(unit, name=None):
    """
    @param unit: synthesized unit
    @return: (entity, arch, context) of testbench
    """
    if name is None:
        name = unit._name + "_tb"
    
    entity = Entity(name)
    arch = Architecture(entity)

    arch.components.append(unit._entity)
    arch.componentInstances.append(unit._entity)
    
    nl = RtlNetlist()
    ctx = {}
    for p in unit._entity.ports:
        t = p._dtype
        if isinstance(t, Bits) and not t == BIT:
            t = Bits(t.bit_length(), t.forceVector, t.signed)  
        s = RtlSignal(nl, p.name, t, t.fromPy(0))
        ctx[p._interface] = s
        p.connectSig(s)

    arch.variables.extend(ctx.values())
    
    return entity, arch, ctx

def mkDriverProc(intf, tbCtx):
    d = HWProcess(intf._sigInside.name + "_driver")
    d.actualTime = -1
    d.driverFor = tbCtx[intf]
    
    return d


class HdlSimConfigVhdlTestbench(HdlSimConfig):
    supported_type_classes = (Boolean, Bits, Enum)
    
    def __init__(self, top):
        super().__init__()
        self.logPropagation = False
        self.logApplyingValues = False  
        self.top = top      

        # unit :  signal | unit
        # signal : None
        self.registered = {}
        
    
    def beforeSim(self, simulator, synthesisedUnit):
        """
        This method is called before first step of simulation.
        """
        top = self.top
        self.tbEnt, self.tbArch, self.tbCtx = makeTestbenchTemplate(top) 

        def reg(sigIntf):
            proc = mkDriverProc(sigIntf, self.tbCtx)
            self.registered[sigIntf._sigInside] = proc
            self.tbArch.processes.append(proc)
            
        for s in walkPhysInterfaces(top):
            if isinstance(s._dtype, self.supported_type_classes):
                reg(s)
        
    def logChange(self, nowTime, sig, nextVal):
        """
        This method is called for every value change of any signal.
        """
        try:
            hwProc = self.registered[sig]
        except KeyError:
            # not every signal has to be registered
            return
        
        if hwProc.actualTime < nowTime:
            hwProc.statements.append(
                WaitStm(int(nowTime - hwProc.actualTime))
            )
        
        hwProc.statements.extend(
            connect(nextVal, hwProc.driverFor)
        )
        
        
        
    def dump(self, dumpFile=sys.stdout):
        hasToBeOpened = isinstance(dumpFile, str)
        if hasToBeOpened:
            _dumpFile = open(dumpFile, 'w')
        else:
            _dumpFile = dumpFile
        
        sc = VhdlSerializer.getBaseNameScope()
        _dumpFile.write(VhdlSerializer.Entity(self.tbEnt, sc))
        _dumpFile.write(VhdlSerializer.Architecture(self.tbArch, sc))
        
        
        
