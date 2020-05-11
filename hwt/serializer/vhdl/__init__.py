"""
VHDL serializer serializes HDL objects to VHDL code.
"""
from hdlConvertorAst.to.vhdl.vhdl2008 import ToVhdl2008
from hwt.serializer.vhdl.serializer import ToHdlAstVhdl2008
from hwt.serializer.xdc.serializer import XdcSerializer


class Vhdl2008Serializer():
    fileExtension = '.vhd'
    TO_HDL_AST = ToHdlAstVhdl2008
    TO_HDL = ToVhdl2008
    TO_CONSTRAINTS = XdcSerializer
