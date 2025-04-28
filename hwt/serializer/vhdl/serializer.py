from natsort.natsort import natsorted
import re
from typing import List

from hdlConvertorAst.hdlAst import HdlOp, HdlModuleDec, HdlOpType, iHdlStatement
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlAll
from hdlConvertorAst.hdlAst._statements import HdlImport, \
    HdlStmIf, HdlStmBlock, HdlStmFor, HdlStmForIn
from hdlConvertorAst.hdlAst._structural import HdlLibrary, HdlModuleDef, \
    HdlCompInst, HdlContext
from hdlConvertorAst.to.vhdl.keywords import VHLD2008_KEYWORDS
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword, NameScope
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call
from hwt.pyUtils.arrayQuery import groupedby
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.vhdl.ops import ToHdlAstVhdl2008_ops
from hwt.serializer.vhdl.statements import ToHdlAstVhdl2008_statements
from hwt.serializer.vhdl.types import ToHdlAstVhdl2008_types
from hwt.serializer.vhdl.value import ToHdlAstVhdl2008_Value


class VhdlNameScope(NameScope):
    RE_MANY_UNDERSCORES = re.compile(r"(_{2,})")

    def checked_name(self, suggested_name, actualObj):
        suggested_name = self._sanitize_name(suggested_name)
        suggested_name = self.RE_MANY_UNDERSCORES.sub(r"_", suggested_name)
        if suggested_name[0] == "_":
            suggested_name = "u" + suggested_name
        return NameScope.checked_name(self, suggested_name, actualObj)


IEEE = HdlValueId("IEEE", obj=LanguageKeyword())
std_logic_1164 = HdlValueId("std_logic_1164", obj=LanguageKeyword())
numeric_std = HdlValueId("numeric_std", obj=LanguageKeyword())


class ToHdlAstVhdl2008(ToHdlAstVhdl2008_Value,
                       ToHdlAstVhdl2008_ops, ToHdlAstVhdl2008_types,
                       ToHdlAstVhdl2008_statements, ToHdlAst):
    """
    :ivar ~.name_scope: name scope used to generate a unique names for tmp variables
        (all object should be registered in namescope before serialization)
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in VHLD2008_KEYWORDS}

    DEFAULT_IMPORTS = [
        HdlLibrary("IEEE"),
        HdlImport([IEEE, std_logic_1164, HdlAll]),
        HdlImport([IEEE, numeric_std, HdlAll]),
    ]
    ASSERT = HdlValueId("assert")
    FAILURE = HdlValueId("failure")

    @classmethod
    def getBaseNameScope(cls):
        s = VhdlNameScope.make_top(True)
        s.update(cls._keywords_dict)
        return s

    @staticmethod
    def _find_HdlCompInst(o):
        if isinstance(o, (list, tuple)):
            for _o in o:
                yield from ToHdlAstVhdl2008._find_HdlCompInst(_o)
        if isinstance(o, HdlCompInst):
            yield o
        elif isinstance(o, HdlStmBlock) and o.in_preproc:
            yield from ToHdlAstVhdl2008._find_HdlCompInst(o.body)
        elif isinstance(o, HdlStmIf) and o.in_preproc:
            if o.if_true:
                yield from ToHdlAstVhdl2008._find_HdlCompInst(o.if_true)
            for _, stms in o.elifs:
                yield from ToHdlAstVhdl2008._find_HdlCompInst(stms)
            if o.if_false:
                yield from ToHdlAstVhdl2008._find_HdlCompInst(o.if_false)
        elif isinstance(o, (HdlStmFor, HdlStmForIn)) and o.in_preproc:
            if o.body:
                yield from ToHdlAstVhdl2008._find_HdlCompInst(o.body)

    def _static_assert_false(self, msg:str):
        return hdl_call(self.ASSERT, [
                 self.FALSE,
                 msg,
                 self.FAILURE])

    def _static_assert_symbol_eq(self, symbol_name:str, v):
        return hdl_call(self.ASSERT, [
                 HdlOp(HdlOpType.EQ, [HdlValueId(symbol_name), v]),
                 "Generated only for this value",
                 self.FAILURE])

    def _as_hdl_HdlModuleDef_param_asserts(self, new_m: HdlModuleDec) -> List[iHdlStatement]:
        return ToHdlAst._as_hdl_HdlModuleDef_param_asserts_real(self, new_m)

    def as_hdl_HdlModuleDef(self, o: HdlModuleDef):
        """
        Translate hwt types and expressions to HDL AST and add explicit components
        """
        _o = super(ToHdlAstVhdl2008, self).as_hdl_HdlModuleDef(o)
        component_insts = []
        for c in _o.objs:
            component_insts.extend(self._find_HdlCompInst(c))

        # select component instances with an unique module_name
        components = [
            x[1][0] for x in
            groupedby(component_insts, lambda c: c.module_name)
        ]
        components = natsorted(components, key=lambda c: c.module_name)
        components = [self.as_hdl_HldComponent(c)
                      for c in components]
        if components:
            # :note: it is important that the asserts are at the end because
            # we are detecting the declarations from the beginning and assert there would
            # disturb that
            objs = [*components, *_o.objs]
            _o.objs = objs

        res = HdlContext()
        res.objs.extend(self.DEFAULT_IMPORTS)
        res.objs.append(_o)
        return res

    def as_hdl_HldComponent(self, o: HdlCompInst):
        c = self.as_hdl_HdlModuleDec(o.origin._rtlCtx.hwModDec)
        return c
