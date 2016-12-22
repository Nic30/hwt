from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.string import String
from hwt.hdlObjects.types.slice import Slice



BOOL = Boolean()
INT = Integer()
UINT = Integer(_min=0)
PINT = Integer(_min=1)
BIT = Bits(widthConstr=1)
VECTOR = Bits(forceVector=True)
STR = String()    
SLICE = Slice()




