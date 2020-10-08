import re

from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlAll
from hdlConvertorAst.hdlAst._statements import HdlImport, ALL_STATEMENT_CLASSES,\
    HdlStmIf, HdlStmBlock, HdlStmFor, HdlStmForIn
from hdlConvertorAst.hdlAst._structural import HdlLibrary, HdlModuleDef,\
    HdlCompInst, HdlContext
from hdlConvertorAst.to.vhdl.keywords import VHLD2008_KEYWORDS
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.pyUtils.arrayQuery import groupedby
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.vhdl.ops import ToHdlAstVhdl2008_ops
from hwt.serializer.vhdl.statements import ToHdlAstVhdl2008_statements
from hwt.serializer.vhdl.types import ToHdlAstVhdl2008_types
from hwt.serializer.vhdl.value import ToHdlAstVhdl2008_Value


class VhdlNameScope(NameScope):
    RE_MANY_UNDERSCORES = re.compile(r"(_{2,})")

    def checked_name(self, actualName, actualObj):
        actualName = self.RE_MANY_UNDERSCORES.sub(r"_", actualName)
        if actualName[0] == "_":
            actualName = "u" + actualName
        return NameScope.checked_name(self, actualName, actualObj)


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

    @classmethod
    def getBaseNameScope(cls):
        s = VhdlNameScope.make_top(True)
        s.update(cls._keywords_dict)
        return s

    @staticmethod
    def _find_HdlCompInst(o):
        if isinstance(o, (list,tuple)):
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
                    
            
            
    def as_hdl_HdlModuleDef(self, o: HdlModuleDef):
        """
        Translate hwt types and expressions to HDL AST and add explicit components
        """
        _o = super(ToHdlAstVhdl2008, self).as_hdl_HdlModuleDef(o)
        component_insts = []
        for c in _o.objs:
            component_insts.extend(self._find_HdlCompInst(c))

        # select comonent instances whith an unique module_name
        components = [
            x[1][0] for x in
            groupedby(component_insts, lambda c: c.module_name)
        ]
        components.sort(key=lambda c: c.module_name)
        components = [self.as_hdl_HldComponent(c)
                      for c in components]
        if components:
            _o.objs = components + _o.objs

        res = HdlContext()
        res.objs.extend(self.DEFAULT_IMPORTS)
        res.objs.append(_o)
        return res

    def as_hdl_HldComponent(self, o: HdlCompInst):
        c = self.as_hdl_HdlModuleDec(o.origin._ctx.ent)
        return c
