"""
Definitions of most common types
"""

from hwt.hdl.types.bits import HBits
from hwt.hdl.types.float import HFloat
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.string import HString


BOOL = HBits(bit_length=1, name="bool")
INT = HBits(bit_length=32, signed=True, name="int",
           strict_sign=False, strict_width=False)
BIT = HBits(bit_length=1)
BIT_N = HBits(bit_length=1, negated=True)
STR = HString()
SLICE = HSlice()
FLOAT64 = HFloat(11, 52, name="float64")