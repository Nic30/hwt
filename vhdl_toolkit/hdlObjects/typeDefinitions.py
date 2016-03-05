from vhdl_toolkit.types import VHDLType

def STD_LOGIC():
    t = VHDLType()
    t.width = 1
    return t

def VHDLBoolean():
    t = VHDLType()
    t.width = bool
    return t

