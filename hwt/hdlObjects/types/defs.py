from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.string import String
from hwt.hdlObjects.types.slice import Slice

BOOL = Boolean()
INT = Integer()
UINT = Integer(_min=0)
PINT = Integer(_min=1)
BIT = Bits(width=1)
BIT_N = Bits(width=1, negated=True)
STR = String()
SLICE = Slice()
