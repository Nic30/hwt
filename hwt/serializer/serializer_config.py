from hwt.serializer.generic.to_hdl_ast import ToHdlAst


class DummySerializerConfig():
    """
    The serializer which does not do any additional code transformations
    and does not produce any output. It is used to generate just internal representation
    of RTL code.
    """
    fileExtension = None
    TO_HDL_AST = ToHdlAst
    TO_HDL = None
    TO_CONSTRAINTS = None
