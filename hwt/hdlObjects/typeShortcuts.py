from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import INT, BOOL, STR, BIT


def hInt(pyVal):
    """ create hdl integer value (for example integer value in vhdl)"""
    return INT.fromPy(pyVal)


def hBool(pyVal):
    """ create hdl boolean value (for example boolean value in vhdl)"""
    return BOOL.fromPy(pyVal)


def hStr(pyVal):
    """create hdl string value (for example string value in vhdl)"""
    return STR.fromPy(pyVal)


def hBit(pyVal):
    """create hdl bit value (for example STD_LOGIC value in vhdl)"""
    return BIT.fromPy(pyVal)


def vec(val, width, signed=None):
    """create hdl vector value"""
    return Bits(width, signed, forceVector=True).fromPy(val)
