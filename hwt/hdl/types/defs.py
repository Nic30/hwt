"""
Definitions of most common types
"""

from hwt.hdl.types.bits import HBits
from hwt.hdl.types.float import HFloat
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.string import HString

# :see: IEEE Std 1076-2008 https://ieeexplore.ieee.org/document/4772740 https://0x04.net/~mwk/vstd/ieee-1076-2008.pdf
# :see: IEEE Std 1800-2012 https://fpga.mit.edu/6205/_static/F23/documentation/1800-2017.pdf

# types intended for HDL compatibility 
BOOL = HBits(bit_length=1, name="bool") # translates to VHDL BOOLEAN
INT = HBits(bit_length=32, signed=True, name="int",
           strict_sign=False, strict_width=False) # translates to VHDL INTEGER, SV integer
STR = HString() # translates to VHDL STRING, SV string
SLICE = HSlice() # type for downto/to expressions
FLOAT64 = HFloat(11, 52, name="float64") # translates to VHDL REAL, SV real

BIT = HBits(bit_length=1)
BIT_N = HBits(bit_length=1, negated=True)
