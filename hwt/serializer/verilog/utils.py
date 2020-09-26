from hwt.hdl.assignment import Assignment
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.value import HValue

from hwt.doc_markers import internal
from hdlConvertorAst.to.verilog.constants import SIGNAL_TYPE
from hwt.hdl.variables import SignalItem
from typing import Union
from ipCorePackager.constants import DIRECTION


@internal
def verilogTypeOfSig(s: Union[SignalItem, HdlPortItem]):
    """
    Check if is register or wire
    """
    if isinstance(s, HdlPortItem):
        if s.direction == DIRECTION.IN or s.direction == DIRECTION.INOUT:
            return SIGNAL_TYPE.PORT_WIRE

        t = verilogTypeOfSig(s.getInternSig())
        if t == SIGNAL_TYPE.WIRE:
            return SIGNAL_TYPE.PORT_WIRE
        elif t == SIGNAL_TYPE.REG:
            return SIGNAL_TYPE.PORT_REG
        else:
            raise ValueError(t)

    driver_cnt = len(s.drivers)
    if driver_cnt == 1:
        d = s.drivers[0]
        if isinstance(d, HdlPortItem):
            # input port
            return SIGNAL_TYPE.WIRE
        elif isinstance(d, Assignment)\
                and d.parentStm is None\
                and not d.indexes\
                and d._event_dependent_from_branch is None\
                and (isinstance(d.src, HValue) or not d.src.hidden):
            # primitive assignment
            return SIGNAL_TYPE.WIRE

    return SIGNAL_TYPE.REG
