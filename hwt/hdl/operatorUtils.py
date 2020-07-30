from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


@internal
def replace_input_in_expr(parentObj: Union["Operator", "HdlStatement"],
                          expr: Union[RtlSignalBase, HValue],
                          toReplace: RtlSignalBase,
                          replacement: RtlSignalBase,
                          updateEndpoints: bool) -> bool:
    """
    :return: True if expr is toReplace and should be replaced else False
    """
    if expr is toReplace:
        if updateEndpoints:
            expr.endpoints.discard(parentObj)
            replacement.endpoints.append(parentObj)
        return True
    elif isinstance(expr, RtlSignalBase) and expr.hidden:
        expr.origin._replace_input(toReplace, replacement)

    return False
