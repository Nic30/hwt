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


def vecT(width, signed=None):
    """Make vector type with specified width for example
       std_logic_vector(width-1 downto 0) in vhdl
    """
    return Bits(width=width, signed=signed, forceVector=True)


def vec(val, width, signed=None):
    """create hdl vector value"""
    assert val < (2 ** int(width))
    return vecT(width, signed).fromPy(val)
