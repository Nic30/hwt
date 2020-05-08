from copy import copy
from typing import Optional

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOp, HdlOpType
from hdlConvertorAst.hdlAst._structural import HdlModuleDec, HdlCompInst
from hdlConvertorAst.to.systemc.keywords import SYSTEMC_KEYWORDS
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.hdl.portItem import HdlPortItem
from hwt.interfaces.std import Clk
from hwt.serializer.generic.to_hdl_ast import ToHdlAst,\
    HWT_TO_HDLCONVEROTR_DIRECTION
from hwt.serializer.simModel.serializer import ToHdlAstSimModel
from hwt.serializer.systemC.expr import ToHdlAstSystemC_expr
from hwt.serializer.systemC.statements import ToHdlAstSystemC_statements
from hwt.serializer.systemC.type import ToHdlAstSystemC_type
from ipCorePackager.constants import DIRECTION


class ToHdlAstSystemC(ToHdlAstSystemC_expr, ToHdlAstSystemC_type,
                      ToHdlAstSystemC_statements,
                      ToHdlAst):
    """
    Serialized used to convert HWT design to SystemC code
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in SYSTEMC_KEYWORDS}
    sc_in_clk = HdlValueId("sc_in_clk", obj=LanguageKeyword())
    sc_out_clk = HdlValueId("sc_out_clk", obj=LanguageKeyword())
    sc_inout_clk = HdlValueId("sc_inout_clk", obj=LanguageKeyword())
    sc_in = HdlValueId("sc_in", obj=LanguageKeyword())
    sc_out = HdlValueId("sc_out", obj=LanguageKeyword())
    sc_inout = HdlValueId("sc_inout", obj=LanguageKeyword())

    def __init__(self, name_scope: Optional[NameScope]=None):
        ToHdlAst.__init__(self, name_scope=name_scope)
        self._is_target = False
        self._in_sensitivity_list = False
        self.signalType = None

    def as_hdl_HdlModuleDec(self, o: HdlModuleDec):
        return ToHdlAstSimModel.as_hdl_HdlModuleDec(self, o)

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
            t = HdlOp(HdlOpType.PARAMETRIZATION, [pt, t])

        var = HdlIdDef()
        var.direction = HWT_TO_HDLCONVEROTR_DIRECTION[o.direction]
        s = o.getInternSig()
        var.name = s.name
        var.origin = o
        var.type = t
        return var

    def as_hdl_HdlCompInst(self, o: HdlCompInst) -> HdlCompInst:
        new_o = copy(o)
        new_o.param_map = []

        orig_is_target = self._is_target
        try:
            self._is_target = True
            port_map = []
            for pi in o.port_map:
                pm = self.as_hdl_PortConnection(pi)
                port_map.append(pm)
            new_o.port_map = port_map
        finally:
            self._is_target = orig_is_target

        return new_o
