import sys

from hwt.hdlObjects.architecture import Architecture
from hwt.hdlObjects.entity import Entity
from hwt.hdlObjects.process import HWProcess
from hwt.hdlObjects.constants import INTF_DIRECTION
from hwt.hdlObjects.statements import WaitStm
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.defs import BIT
from hwt.hdlObjects.types.enum import Enum
from hwt.serializer.vhdl.serializer import VhdlSerializer
from hwt.simulator.hdlSimConfig import HdlSimConfig
from hwt.code import connect
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces
from hwt.synthesizer.rtlLevel.netlist import RtlNetlist
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


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
            """register interface and create diver process for it"""
            proc = mkDriverProc(sigIntf, self.tbCtx)
            self.registered[sigIntf._sigInside] = proc
            self.tbArch.processes.append(proc)
            
        for s in walkPhysInterfaces(top):
            if s._direction is INTF_DIRECTION.SLAVE and isinstance(s._dtype, self.supported_type_classes):
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
            a = hwProc.actualTime
            if a < 0:
                a = 0
            delay = int(nowTime - a)
            if delay > 0:
                hwProc.statements.append(
                    WaitStm(int(delay) // 1000)
                )
                hwProc.actualTime = nowTime
        
        try:
            # SimBits type does not have forceVector flag, but serializer requires it
            nextVal._dtype.forceVector = hwProc.driverFor._dtype.forceVector
        except AttributeError:
            pass
        
        hwProc.statements.extend(
            connect(nextVal, hwProc.driverFor)
        )
        
        
        
    def dump(self, dumpFile=sys.stdout):
        for proc in self.tbArch.processes:
            proc.statements.append(WaitStm(None))
        
        hasToBeOpened = isinstance(dumpFile, str)
        if hasToBeOpened:
            _dumpFile = open(dumpFile, 'w')
        else:
            _dumpFile = dumpFile
        
        sc = VhdlSerializer.getBaseNameScope()
        _dumpFile.write(VhdlSerializer.formater(VhdlSerializer.Entity(self.tbEnt, sc)))
        _dumpFile.write(VhdlSerializer.formater(VhdlSerializer.Architecture(self.tbArch, sc)))
        
        
        
