"""
Hwt serializer converts  HDL objects back to code in python for hwt.
"""
from hdlConvertorAst.to.hwt._main import ToHwt
from hwt.serializer.hwt.serializer import ToHdlAstHwt
from hwt.serializer.serializer_config import DummySerializerConfig
from hdlConvertorAst.hdlAst import iHdlObj


class HwtSerializer(DummySerializerConfig):
    fileExtension = '.py'
    TO_HDL_AST = ToHdlAstHwt
    TO_HDL = ToHwt


class ToHdlAstDebugHwt(ToHdlAstHwt):

    def as_hdl(self, obj) -> iHdlObj:
        try:
            return super(ToHdlAstDebugHwt, self).as_hdl(obj)
        except:
            return obj.__repr__()


class HwtDebugSerializer(DummySerializerConfig):
    fileExtension = '.py'
    TO_HDL_AST = ToHdlAstDebugHwt
    TO_HDL = ToHwt
