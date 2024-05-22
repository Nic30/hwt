
from typing import Optional

from hdlConvertorAst.hdlAst import HdlStmBlock
from hdlConvertorAst.hdlAst._expr import HdlValueId
from hdlConvertorAst.hdlAst._structural import HdlModuleDef
from hdlConvertorAst.to.hwt.keywords import HWT_KEYWORDS
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.code import CodeBlock
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.hwt.ops import ToHdlAstHwt_ops
from hwt.serializer.hwt.types import ToHdlAstHwt_types
from hwt.serializer.hwt.value import ToHdlAstHwt_value
from hwt.serializer.simModel.serializer import ToHdlAstSimModel


class ToHdlAstHwt(ToHdlAstHwt_value, ToHdlAstHwt_ops,
                  ToHdlAstHwt_types, ToHdlAst):
    """
    Serializer which converts HWT objects back to HWT code
    for debugging purposes/code ports

    :ivar ~._valueWidthRequired: flag which tells if the values are required to have
        the width specified
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in HWT_KEYWORDS}

    def __init__(self, name_scope: Optional[NameScope]=None):
        super(ToHdlAstHwt, self).__init__(name_scope=name_scope)
        self._valueWidthRequired = False
        self.currentHwModule = None
        self.debug = False

    def has_to_be_process(self, proc):
        return True

    def can_pop_process_wrap(self, statements, hasToBeVhdlProcess):
        return False

    def _as_hdl_HdlModuleDef(self, new_m: HdlModuleDef) -> HdlModuleDef:
        return ToHdlAstSimModel._as_hdl_HdlModuleDef(self, new_m)

    def sensitivityListItem(self, item, anyIsEventDependnt):
        if isinstance(item, HOperatorNode):
            op = item.operator
            assert op in (HwtOps.RISING_EDGE, HwtOps.FALLING_EDGE), item
            assert not item.operands[0].hidden, item
            return self.as_hdl_HOperatorNode(item)
        else:
            return HdlValueId(item.name, obj=item)

    def as_hdl_CodeBlock(self, o: CodeBlock):
        res = HdlStmBlock()
        for _o in o.statements:
            res.body.append(self.as_hdl(_o))
        return res

