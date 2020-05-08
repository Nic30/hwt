"""
Hwt serializer converts  HDL objects back to code in python for hwt.
"""
from hdlConvertorAst.to.hwt._main import ToHwt
from hwt.serializer.hwt.serializer import ToHdlAstHwt
from hwt.serializer.serializer_config import DummySerializerConfig


class HwtSerializer(DummySerializerConfig):
    fileExtension = '.py'
    TO_HDL_AST = ToHdlAstHwt
    TO_HDL = ToHwt
