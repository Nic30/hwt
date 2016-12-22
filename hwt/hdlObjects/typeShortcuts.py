from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import INT, BOOL, STR, BIT
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.synthesizer.param import evalParam


# create hdl integer value (for example integer value in vhdl)
hInt = lambda val: INT.fromPy(val)

# create hdl boolean value (for example boolean value in vhdl)
hBool = lambda val: BOOL.fromPy(val)

# create hdl string value (for example string value in vhdl)
hStr = lambda val: STR.fromPy(val)

# create hdl bit value (for example STD_LOGIC value in vhdl)
hBit = lambda val: BIT.fromPy(val)

def mkRange(width):
    """Make hdl range (for example 1 downto 0 in vhdl)
       @return: (width -1, 0) 
    """
    to = toHVal(width)
    to = to - 1
    return to._downto(0)

def vecT(width, signed=None):
    """Make vector type with specified width for example
       std_logic_vector(width-1 downto 0) in vhdl
    """
    return Bits(widthConstr=mkRange(width), signed=signed, forceVector=True)

def vec(val, width, signed=None):
    """create hdl vector value"""
    assert val < evalParam(hInt(2)._pow(width)).val
    return vecT(width, signed).fromPy(val)
