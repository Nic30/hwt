"""
SystemC serializer serializes HDL objects to systemC code.
"""
from hdlConvertorAst.to.systemc._main import ToSystemc
from hwt.serializer.serializer_config import DummySerializerConfig
from hwt.serializer.systemC.serializer import ToHdlAstSystemC
from hwt.serializer.xdc.serializer import XdcSerializer


class SystemCSerializer(DummySerializerConfig):
    fileExtension = '.cpp'
    TO_HDL_AST = ToHdlAstSystemC
    TO_HDL = ToSystemc
    TO_CONSTRAINTS = XdcSerializer
