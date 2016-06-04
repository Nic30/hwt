from hdl_toolkit.hdlObjects.types.boolean import Boolean
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.string import String
from hdl_toolkit.hdlObjects.types.slice import Slice



BOOL = Boolean()
INT = Integer()
UINT = Integer(_min=0)
PINT = Integer(_min=1)
BIT = Bits(widthConstr=1)
VECTOR = Bits(forceVector=True)
STR = String()    
SLICE = Slice()




