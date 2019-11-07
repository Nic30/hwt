from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, BOOL, STR, BIT


def hInt(pyVal):
    """ create hdl integer value (for example integer value in vhdl)"""
    return INT.from_py(pyVal)


def hBool(pyVal):
    """ create hdl bool value (for example bool value in vhdl)"""
    return BOOL.from_py(pyVal)


def hStr(pyVal):
    """create hdl string value (for example string value in vhdl)"""
    return STR.from_py(pyVal)


def hBit(pyVal):
    """create hdl bit value (for example STD_LOGIC value in vhdl)"""
    return BIT.from_py(pyVal)


def vec(val, width, signed=None):
    """create hdl vector value"""
    return Bits(width, signed, force_vector=True).from_py(val)
