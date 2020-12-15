from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
# from hwt.hdl.operator import Operator


@internal
def replace_input_in_expr(parentObj: Union["Operator", "HdlStatement"],
                          expr: Union[RtlSignalBase, HValue],
                          toReplace: RtlSignalBase,
                          replacement: RtlSignalBase,
                          updateEndpoints: bool) -> RtlSignalBase:
    """
    :return: True if expr is toReplace and should be replaced else False
    """
    if expr is toReplace:
        if updateEndpoints:
            expr.endpoints.discard(parentObj)
            replacement.endpoints.append(parentObj)
        return replacement
    elif isinstance(expr, RtlSignalBase) and expr.hidden:
        op = expr.origin
        # assert isinstance(op, Operator), op
        new_operands = []
        for o in op.operands:
            new_o = replace_input_in_expr(op, o, toReplace, replacement, True)
            new_operands.append(new_o)

        res = op.operator._evalFn(*new_operands)
        return res
    else:
        return expr
