"""
Sim model serializer serialize HDL objects to simulation model writen in python.
For pycocotb.basic_rtl_simulator
"""
from hdlConvertorAst.to.basic_hdl_sim_model._main import ToBasicHdlSimModel
from hwt.serializer.serializer_config import DummySerializerConfig
from hwt.serializer.simModel.serializer import ToHdlAstSimModel


class SimModelSerializer(DummySerializerConfig):
    fileExtension = '.py'
    TO_HDL_AST = ToHdlAstSimModel
    TO_HDL = ToBasicHdlSimModel
