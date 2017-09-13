
from typing import Optional, Any

from hwt.hdlObjects.types.defs import INT, STR, BOOL
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.value import Value
from hwt.hdlObjects.variables import SignalItem
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase


defaultConversions = {int: INT,
                      str: STR,
                      bool: BOOL}


def toHVal(op: Any, suggestedType: Optional[HdlType]=None):
    """Convert python or hdl value/signal object to hdl value/signal object"""
    if isinstance(op, Value) or isinstance(op, SignalItem):
        return op
    elif isinstance(op, InterfaceBase):
        return op._sig
    else:
        if isinstance(op, int):
            if suggestedType is not None:
                return suggestedType.fromPy(op)

            if op >= 1 << 31:
                raise TypeError("Number %d is too big to fit in 32 bit integer of HDL use Bits type instead" % op)
            elif op < -(1 << 31):
                raise TypeError("Number %d is too small to fit in 32 bit integer of HDL use Bits type instead" % op)
        try:
            hType = defaultConversions[type(op)]
        except KeyError:
            hType = None

        if hType is None:
            raise TypeError("%s" % (op.__class__))

        return hType.fromPy(op)
