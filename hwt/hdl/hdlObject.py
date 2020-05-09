from io import StringIO
from hdlConvertorAst.translate.common.name_scope import NameScope


class HdlObject():
    """
    Base Hdl object class for object which can be directly serialized
    to target HDL language
    """

    def __repr__(self):
        from hwt.serializer.hwt import HwtSerializer
        name_scope = NameScope(None, "debug", False, debug=True)
        to_hdl = HwtSerializer.TO_HDL_AST(name_scope)
        to_hdl.debug = True
        hdl = to_hdl.as_hdl(self)
        buff = StringIO()
        # import sys
        # buff = sys.stdout
        ser = HwtSerializer.TO_HDL(buff)
        ser.visit_iHdlObj(hdl)
        return buff.getvalue()
