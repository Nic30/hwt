from io import StringIO
import re

from hdlConvertor.hdlAst._expr import HdlName, HdlAll
from hdlConvertor.hdlAst._statements import HdlImport
from hdlConvertor.hdlAst._structural import HdlLibrary, HdlModuleDef,\
    HdlComponentInst
from hdlConvertor.to.vhdl.keywords import VHLD2008_KEYWORDS
from hdlConvertor.to.vhdl.vhdl2008 import ToVhdl2008
from hdlConvertor.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.hdl.types.array import HArray
from hwt.hdl.types.enum import HEnum
from hwt.pyUtils.arrayQuery import groupedby
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.vhdl.ops import ToHdlAstVhdl2008_ops
from hwt.serializer.vhdl.statements import ToHdlAstVhdl2008_statements
from hwt.serializer.vhdl.types import ToHdlAstVhdl2008_types
from hwt.serializer.vhdl.value import ToHdlAstVhdl2008_Value


class VhdlNameScope(NameScope):
    RE_MANY_UNDERSCORES = re.compile(r"(_{2,})")

    def checkedName(self, actualName, actualObj):
        actualName = self.RE_MANY_UNDERSCORES.sub(r"_", actualName)
        return NameScope.checkedName(self, actualName, actualObj)


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

    def does_type_requires_extra_def(self, t, other_types):
        return isinstance(t, (HEnum, HArray)) and t not in other_types

    def as_hdl_HdlModuleDef(self, o: HdlModuleDef):
        """
        Translate hwt types and expressions to HDL AST and add explicit components
        """
        _o = super(ToHdlAstVhdl2008, self).as_hdl_HdlModuleDef(o)
        component_insts = []
        for c in o.objs:
            if not isinstance(c, HdlComponentInst):
                break
            else:
                component_insts.append(c)

        components = [
            x[1][0] for x in
            groupedby(component_insts, lambda c: c.module_name)
        ]
        components.sort(key=lambda c: c.module_name)
        components = [self.as_hdl_Component(c)
                      for c in components]
        if components:
            _o.objs += components
        return _o


class Vhdl2008Serializer():
    fileExtension = '.vhd'
    TO_HDL_AST = ToHdlAstVhdl2008
    TO_HDL = ToVhdl2008


def _to_Vhdl2008_str(obj):
    """
    Convert an ebalorated hdl objects to a VHDL2008 string
    """
    buff = StringIO()
    to_ast = ToHdlAstVhdl2008()
    hdl = to_ast.as_hdl(obj)
    ser = ToVhdl2008(buff)
    ser.visit_iHdlObj(hdl)
    return buff.getvalue()
