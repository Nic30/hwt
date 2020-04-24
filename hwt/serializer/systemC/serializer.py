from hdlConvertor.hdlAst._defs import HdlVariableDef
from hdlConvertor.hdlAst._expr import HdlName, HdlCall, HdlBuiltinFn
from hdlConvertor.to.systemc._main import ToSystemc
from hdlConvertor.to.systemc.keywords import SYSTEMC_KEYWORDS
from hdlConvertor.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.hdl.portItem import HdlPortItem
from hwt.interfaces.std import Clk
from hwt.serializer.generic.to_hdl_ast import ToHdlAst,\
    HWT_TO_HDLCONVEROTR_DIRECTION
from hwt.serializer.systemC.statements import ToHdlAstSystemC_statements
from hwt.serializer.systemC.type import ToHdlAstSystemC_type
from hwt.serializer.systemC.expr import ToHdlAstSystemC_expr
from ipCorePackager.constants import DIRECTION
from typing import Optional


class ToHdlAstSystemC(ToHdlAstSystemC_expr, ToHdlAstSystemC_type,
                      ToHdlAstSystemC_statements,
                      ToHdlAst):
    """
    Serialized used to convert HWT design to SystemC code
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in SYSTEMC_KEYWORDS}
    sc_in_clk = HdlName("sc_in_clk", obj=LanguageKeyword())
    sc_out_clk = HdlName("sc_out_clk", obj=LanguageKeyword())
    sc_inout_clk = HdlName("sc_inout_clk", obj=LanguageKeyword())
    sc_in = HdlName("sc_in", obj=LanguageKeyword())
    sc_out = HdlName("sc_out", obj=LanguageKeyword())
    sc_inout = HdlName("sc_inout", obj=LanguageKeyword())

    def __init__(self, name_scope: Optional[NameScope]=None):
        ToHdlAst.__init__(self, name_scope=name_scope)
        self._is_target = False
        self._in_sensitivity_list = False

    def as_hdl_HdlPortItem(self, o: HdlPortItem):
        i = o.getInternSig()._interface
        d = o.direction
        if isinstance(i, Clk):
            assert i._dtype.bit_length() == 1, i
            if d == DIRECTION.IN:
                t = self.sc_in_clk
            elif d == DIRECTION.OUT:
                t = self.sc_out_clk
            elif d == DIRECTION.INOUT:
                t = self.sc_inout_clk
            else:
                raise ValueError(d)
        else:
            if d == DIRECTION.IN:
                pt = self.sc_in
            elif d == DIRECTION.OUT:
                pt = self.sc_out
            elif d == DIRECTION.INOUT:
                pt = self.sc_inout
            else:
                raise ValueError(d)
            t = self.as_hdl_HdlType(o._dtype)
            t = HdlCall(HdlBuiltinFn.PARAMETRIZATION, [pt, t])

        var = HdlVariableDef()
        var.direction = HWT_TO_HDLCONVEROTR_DIRECTION[o.direction]
        s = o.getInternSig()
        var.name = s.name
        var.origin = o
        var.type = t
        return var


class SystemCSerializer():
    fileExtension = '.cpp'
    TO_HDL_AST = ToHdlAstSystemC
    TO_HDL = ToSystemc
