from hdlConvertor.to.systemc.keywords import SYSTEMC_KEYWORDS
from hdlConvertor.translate.common.name_scope import LanguageKeyword
from hwt.interfaces.std import Clk
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.systemC.context import SystemCCtx
from hwt.serializer.systemC.ops import ToHdlAstSystemC_ops
from hwt.serializer.systemC.statements import ToHdlAstSystemC_statements
from hwt.serializer.systemC.type import ToHdlAstSystemC_type
from hwt.serializer.systemC.value import ToHdlAstSystemC_value


class ToHdlAstSystemC(ToHdlAstSystemC_value, ToHdlAstSystemC_type,
                      ToHdlAstSystemC_statements, ToHdlAstSystemC_ops,
                      ToHdlAst):
    """
    Serialized used to convert HWT design to SystemC code
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in SYSTEMC_KEYWORDS}

    @classmethod
    def getBaseContext(cls):
        return SystemCCtx(cls.getBaseNameScope(), 0, None, None)

    def as_hdl_HdlPortItem(self, p):
        raise NotImplementedError()
        p.getInternSig().name = p.name
        if isinstance(p.getInternSig()._interface, Clk):
            return "sc_%s_clk %s;" % (d, p.name)

        return "sc_%s<%s> %s;" % (d,
                                  self.as_hdl_HdlType(p._dtype),
                                  p.name)


class SystemCSerializer():
    fileExtension = '.cpp'
    TO_HDL_AST = ToHdlAstSystemC
