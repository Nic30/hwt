from typing import Union

from hdlConvertorAst.hdlAst import iHdlStatement
from hdlConvertorAst.to.verilog.constants import SIGNAL_TYPE
from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.variables import HdlSignalItem
from ipCorePackager.constants import DIRECTION


@internal
def verilogTypeOfSig(s: Union[HdlSignalItem, HdlPortItem]):
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

    driver_cnt = len(s._rtlDrivers)
    if driver_cnt == 1:
        d = s._rtlDrivers[0]
        if isinstance(d, HdlPortItem):
            # input port
            return SIGNAL_TYPE.WIRE
        elif isinstance(d, HdlAssignmentContainer)\
                and d.parentStm is None\
                and not d.indexes\
                and d._event_dependent_from_branch is None\
                and (isinstance(d.src, HConst) or not d.src._isUnnamedExpr):
            # primitive assignment
            return SIGNAL_TYPE.WIRE
        elif isinstance(d, iHdlStatement) and d.in_preproc:
            return SIGNAL_TYPE.WIRE

    return SIGNAL_TYPE.REG
