"""
Verilog serializer serializes HDL objects to verilog code.
"""
from hdlConvertorAst.to.verilog.verilog2005 import ToVerilog2005
from hwt.serializer.serializer_config import DummySerializerConfig
from hwt.serializer.verilog.serializer import ToHdlAstVerilog
from hwt.serializer.xdc.serializer import XdcSerializer


class VerilogSerializer(DummySerializerConfig):
    fileExtension = '.v'
    TO_HDL_AST = ToHdlAstVerilog
    TO_HDL = ToVerilog2005
    TO_CONSTRAINTS = XdcSerializer