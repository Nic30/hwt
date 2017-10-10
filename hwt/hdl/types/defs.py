from hwt.hdl.types.bool import HBool
from hwt.hdl.types.integer import Integer
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.string import String
from hwt.hdl.types.slice import Slice

"""
Definitions of most common types
"""

BOOL = HBool()
INT = Integer()
BIT = Bits(width=1)
BIT_N = Bits(width=1, negated=True)
STR = String()
SLICE = Slice()
