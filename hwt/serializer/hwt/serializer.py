
from typing import Optional

from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOpType
from hdlConvertorAst.hdlAst._structural import HdlModuleDef
from hdlConvertorAst.to.hwt.keywords import HWT_KEYWORDS
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.hwt.ops import ToHdlAstHwt_ops
from hwt.serializer.hwt.types import ToHdlAstHwt_types
from hwt.serializer.hwt.value import ToHdlAstHwt_value
from hwt.serializer.simModel.serializer import ToHdlAstSimModel


class ToHdlAstHwt(ToHdlAstHwt_value, ToHdlAstHwt_ops,
                  ToHdlAstHwt_types, ToHdlAst):
    """
    Serializer which converts Hwt objects back to Hwt code
    for debugging purposes/code ports

    :ivar ~._valueWidthRequired: flag which tells if the values are required to have
        the width specified
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in HWT_KEYWORDS}

    def __init__(self, name_scope: Optional[NameScope] = None):
        super(ToHdlAstHwt, self).__init__(name_scope=name_scope)
        self._valueWidthRequired = False
        self.currentUnit = None
        self.debug = False

    def has_to_be_process(self, proc):
        return True

    def can_pop_process_wrap(self, statements, hasToBeVhdlProcess):
        return False

    def _as_hdl_HdlModuleDef(self, new_m: HdlModuleDef) -> HdlModuleDef:
        return ToHdlAstSimModel._as_hdl_HdlModuleDef(self, new_m)

    def sensitivityListItem(self, item, anyIsEventDependnt):
        if isinstance(item, Operator):
            op = item.operator
            assert op in (AllOps.RISING_EDGE,  AllOps.FALLING_EDGE), item
            assert not item.operands[0].hidden, item
            return self.as_hdl_Operator(item)
        else:
            return HdlValueId(item.name, obj=item)
