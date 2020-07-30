
from typing import Optional, Any

from hwt.hdl.types.defs import INT, STR, BOOL
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.value import HValue
from hwt.hdl.variables import SignalItem
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase


defaultPyConversions = {int: INT,
                        str: STR,
                        bool: BOOL}


def toHVal(op: Any, suggestedType: Optional[HdlType]=None):
    """Convert python or hdl value/signal object to hdl value/signal object"""
    if isinstance(op, HValue) or isinstance(op, SignalItem):
        return op
    elif isinstance(op, InterfaceBase):
        return op._sig
    else:
        if isinstance(op, int):
            if suggestedType is not None:
                return suggestedType.from_py(op)

            if op >= 1 << 31:
                raise TypeError(
                    "Number %d is too big to fit in 32 bit integer of HDL"
                    " use Bits type instead" % op)
            elif op < -(1 << 31):
                raise TypeError(
                    "Number %d is too small to fit in 32 bit integer"
                    " of HDL use Bits type instead" % op)
        try:
            hType = defaultPyConversions[type(op)]
        except KeyError:
            hType = None

        if hType is None:
            raise TypeError("Unknown hardware type for %s" % (op.__class__))

        return hType.from_py(op)
