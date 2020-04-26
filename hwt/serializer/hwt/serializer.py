
from hdlConvertor.hdlAst._expr import HdlName
from hdlConvertor.to.hwt._main import ToHwt
from hdlConvertor.to.hwt.keywords import HWT_KEYWORDS
from hdlConvertor.translate.common.name_scope import LanguageKeyword, NameScope
from hwt.hdl.constants import SENSITIVITY
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.serializer.generic.to_hdl_ast import ToHdlAst
from hwt.serializer.hwt.ops import ToHdlAstHwt_ops
from hwt.serializer.hwt.types import ToHdlAstHwt_types
from hwt.serializer.hwt.value import ToHdlAstHwt_value


class ToHdlAstHwt(ToHdlAstHwt_value, ToHdlAstHwt_ops,
                  ToHdlAstHwt_types, ToHdlAst):
    """
    Serializer which converts Hwt objects back to Hwt code
    for debugging purposes/code ports

    :ivar ~._valueWidthRequired: flag which tells if the values are required to have
        the width specified
    """
    _keywords_dict = {kw: LanguageKeyword() for kw in HWT_KEYWORDS}

    def __init__(self, name_scope: NameScope):
        super(ToHdlAstHwt, self).__init__(name_scope)
        self._valueWidthRequired = False
        self.currentUnit = None

    def has_to_be_process(self, proc):
        return True

    def can_pop_process_wrap(self, statements, hasToBeVhdlProcess):
        return False

    def sensitivityListItem(self, item, anyIsEventDependnt):
        if isinstance(item, Operator):
            op = item.operator
            if op == AllOps.RISING_EDGE:
                sens = SENSITIVITY.RISING
            elif op == AllOps.FALLING_EDGE:
                sens = SENSITIVITY.FALLING
            else:
                raise TypeError("This is not an event sensitivity", op)

            s = item.operands[0]
            return [sens, HdlName(s.name, obj=s)]
        else:
            return HdlName(item.name, obj=item)


class HwtSerializer():
    fileExtension = '.py'
    TO_HDL_AST = ToHdlAstHwt
    TO_HDL = ToHwt
