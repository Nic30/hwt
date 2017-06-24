
from hwt.hdlObjects.types.defs import INT, STR, BOOL
from hwt.hdlObjects.value import Value
from hwt.hdlObjects.variables import SignalItem
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase


defaultConversions = {int: INT,
                      str: STR,
                      bool: BOOL}


def toHVal(op):
    """Convert python value object to object of hdl type value"""
    if isinstance(op, Value) or isinstance(op, SignalItem):
        return op
    elif isinstance(op, InterfaceBase):
        return op._sig
    else:
        if isinstance(op, int):
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
