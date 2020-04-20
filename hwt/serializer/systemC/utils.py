from hdlConvertor.to.verilog.constants import SIGNAL_TYPE
from hwt.hdl.statement import HdlStatement
from hwt.pyUtils.arrayQuery import arr_any


def systemCTypeOfSig(signalItem):
    """
    Check if is register or wire
    """
    if signalItem._const or\
       arr_any(signalItem.drivers,
               lambda d: isinstance(d, HdlStatement)
               and d._now_is_event_dependent):

        return SIGNAL_TYPE.REG
    else:
        return SIGNAL_TYPE.WIRE
