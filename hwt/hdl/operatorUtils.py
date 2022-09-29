from typing import Union, Tuple

from hwt.doc_markers import internal
from hwt.hdl.statements.statement import HdlStatement
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import SignalDriverErr
from hwt.hdl.portItem import HdlPortItem


# from hwt.hdl.operator import Operator
@internal
def does_expr_contain_expr(expr: Union[RtlSignalBase, HValue], subExprToFind: Union[RtlSignalBase, HValue]):
    if expr is subExprToFind:
        return True
    if isinstance(expr, RtlSignalBase) and expr.hidden and expr.origin is not None:
        # :note: must be opeator because otherwise this expr should not be hidden
        for op in expr.origin.operands:
            if does_expr_contain_expr(op, subExprToFind):
                return True
    
    return False


@internal
def _replace_input_in_expr(expr: Union[RtlSignalBase, HValue],
                           toReplace: RtlSignalBase,
                           replacement: RtlSignalBase,
                           ) -> RtlSignalBase:
    """
    :return: newly rewritten expression with the subexpression replaced
    """
    if expr is toReplace:
        return replacement

    elif isinstance(expr, RtlSignalBase) and expr.hidden:
        op = expr.origin
        if op is None:
            try:
                op = expr.singleDriver()
            except SignalDriverErr:
                return expr
        if isinstance(op, (HdlPortItem, HdlStatement)):
            return expr
            raise NotImplementedError()
        # assert isinstance(op, Operator), op
        ops = (_replace_input_in_expr(o, toReplace, replacement)
               for o in op.operands)
        res = op.operator._evalFn(*ops)
        return res

    else:
        return expr


@internal
def replace_input_in_expr(topStatement: "HdlStatement",
                          parentStm: "HdlStatement",
                          expr: Union[RtlSignalBase, HValue],
                          toReplace: RtlSignalBase,
                          replacement: RtlSignalBase,
                          # maybeDisconnectedSignals: UniqList[RtlSignalBase]
                          ) -> Tuple[RtlSignalBase, bool]:
    """
    :return: tuple (newExpression, True if expr is toReplace and should be replaced else False)
    """
    didContainExpr = does_expr_contain_expr(expr, toReplace)
    if didContainExpr:
        res = _replace_input_in_expr(expr, toReplace, replacement)
        # maybeDisconnectedSignals.append(expr)
        expr.endpoints.discard(topStatement)
        if not isinstance(res, HValue):
            res.endpoints.append(topStatement)

        return res, True
    else:
        return expr, False

