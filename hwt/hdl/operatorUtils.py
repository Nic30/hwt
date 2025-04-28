from typing import Union, Tuple

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.portItem import HdlPortItem
from hwt.hdl.statements.statement import HdlStatement, SignalReplaceSpecType
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr


# from hwt.hdl.operator import Operator
@internal
def _replace_input_in_expr(expr: Union[RtlSignalBase, HConst], toReplace: SignalReplaceSpecType) -> RtlSignalBase:
    """
    :return: newly rewritten expression with the subexpression replaced, True if changed else False
    """
    if isinstance(toReplace, dict):
        replacement = toReplace.get(expr, None)
    else:
        _toReplace, replacement = toReplace
        if expr is not _toReplace:
            replacement = None
            
    if replacement is not None:
        return replacement, True

    elif isinstance(expr, RtlSignalBase) and expr._isUnnamedExpr:
        op = expr._rtlObjectOrigin
        if op is None:
            try:
                op = expr.singleDriver()
            except SignalDriverErr:
                return expr, False
        if isinstance(op, (HdlPortItem, HdlStatement)):
            return expr, False

        # assert isinstance(op, Operator), op
        operandChanged = False
        ops = []
        for o in op.operands:
            _o, _change = _replace_input_in_expr(o, toReplace)
            ops.append(_o)
            operandChanged |= _change
            
        if operandChanged:
            res = op.operator._evalFn(*ops)
            return res, True
        else:
            return expr, False

    else:
        return expr, False


@internal
def replace_input_in_expr(topStatement: "HdlStatement",
                          parentStm: "HdlStatement",
                          expr: Union[RtlSignalBase, HConst],
                          toReplace: SignalReplaceSpecType,
                          # maybeDisconnectedSignals: SetList[RtlSignalBase]
                          ) -> Tuple[RtlSignalBase, bool]:
    """
    :return: tuple (newExpression, True if expr is toReplace and should be replaced else False)
    """
    res, didContainExpr = _replace_input_in_expr(expr, toReplace)
    if didContainExpr:
        # maybeDisconnectedSignals.append(expr)
        if not isinstance(expr, HConst):
            expr._rtlEndpoints.discard(topStatement)
        if not isinstance(res, HConst):
            res._rtlEndpoints.append(topStatement)

        return res, True
    else:
        assert res is expr
        return expr, False

