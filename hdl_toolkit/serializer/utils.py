from hdl_toolkit.hdlObjects.entity import Entity
from hdl_toolkit.hdlObjects.architecture import Architecture
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.defs import BIT
from hdl_toolkit.synthetisator.rtlLevel.rtlSignal import RtlSignal
from hdl_toolkit.hdlObjects.process import HWProcess
from hdl_toolkit.synthetisator.codeOps import connect
from hdl_toolkit.hdlObjects.statements import WaitStm
from hdl_toolkit.interfaces.std import Rst_n


def _clkDriverProc(clk, clkPeriod):
    d = HWProcess("clk_driver")
    d.statements.extend(
        connect(0, clk) +
        [WaitStm(clkPeriod//2),] +
        connect(1, clk) +
        [WaitStm(clkPeriod//2),]
    )   
    return d

def _rstDriverProc(rst, isNegated, resetDelay):
    d = HWProcess("rst_driver")
    activeIn = not bool(isNegated)
    d.statements.extend(
        connect(activeIn, rst) +
        [WaitStm(resetDelay),] +
        connect(not activeIn, rst) +
        [WaitStm(None)]
    )   
    return d

def makeTestbenchTemplate(unit, name=None, clkPeriod=10, resetDelay=15):
    """
    @param unit: synthesized unit
    """
    if name is None:
        name = unit._name + "_tb"
    
    entity = Entity(name)
    arch = Architecture(entity)

    arch.components.append(unit._entity)
    arch.componentInstances.append(unit._entity)
    
    ctx = {}
    for p in unit._entity.ports:
        t = p._dtype
        if isinstance(t, Bits) and not t == BIT:
            t = Bits(t.bit_length(), t.forceVector, t.signed)  
        s =  RtlSignal(p.name, t, t.fromPy(0))
        ctx[p._interface] = s
        p.connectSig(s)

    arch.variables.extend(ctx.values())
    
    if hasattr(unit, "clk"):
        clk = ctx[unit.clk]
        d = _clkDriverProc(clk, clkPeriod)
        arch.processes.append(d)
    
    rst = None
    if hasattr(unit, "rst_n"):
        rst = unit.rst_n
    elif hasattr(unit, "rst"):
        rst = unit.rst
    
    if rst is not None:
        rst_sig = ctx[rst]
        d = _rstDriverProc(rst_sig, isinstance(rst, Rst_n), resetDelay)
        arch.processes.append(d)
        
    
    return entity, arch