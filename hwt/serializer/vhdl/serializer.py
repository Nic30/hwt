import re

from hdlConvertor.hdlAst._expr import HdlName, HdlAll
from hdlConvertor.hdlAst._statements import HdlImport
from hdlConvertor.hdlAst._structural import HdlLibrary, HdlModuleDef,\
    HdlComponentInst, HdlContext
from hdlConvertor.to.vhdl.keywords import VHLD2008_KEYWORDS
from hdlConvertor.to.vhdl.vhdl2008 import ToVhdl2008
from hdlConvertor.translate.common.name_scope import LanguageKeyword, NameScope
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
        return NameScope.checked_name(self, actualName, actualObj)


IEEE = HdlName("IEEE", obj=LanguageKeyword())
std_logic_1164 = HdlName("std_logic_1164", obj=LanguageKeyword())
numeric_std = HdlName("numeric_std", obj=LanguageKeyword())


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

    def as_hdl_HdlModuleDef(self, o: HdlModuleDef):
        """
        Translate hwt types and expressions to HDL AST and add explicit components
        """
        _o = super(ToHdlAstVhdl2008, self).as_hdl_HdlModuleDef(o)
        component_insts = []
        for c in _o.objs:
            if isinstance(c, HdlComponentInst):
                component_insts.append(c)

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

    def as_hdl_HldComponent(self, o: HdlComponentInst):
        c = self.as_hdl_HdlModuleDec(o.origin._ctx.ent)
        return c


class Vhdl2008Serializer():
    fileExtension = '.vhd'
    TO_HDL_AST = ToHdlAstVhdl2008
    TO_HDL = ToVhdl2008
