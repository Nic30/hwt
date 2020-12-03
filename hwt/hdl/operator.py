from hwt.hdl.hdlObject import HdlObject
from hwt.hdl.operatorDefs import isEventDependentOp, OpDefinition
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.value import HValue
from hwt.pyUtils.arrayQuery import arr_all
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, RtlSignalBase
from typing import Generator, Union, Tuple

from hwt.doc_markers import internal
from hwt.hdl.operatorUtils import replace_input_in_expr


@internal
def getCtxFromOps(operands):
    for o in operands:
        if isinstance(o, RtlSignalBase):
            return o.ctx
    raise TypeError("Can not find context because there is no signal in ops"
                    "(value operators should be already resolved)")


def isConst(item):
    """
    :return: True if expression is constant
    """
    return isinstance(item, HValue) or item._const


class Operator(HdlObject):
    """
    Class of operator in expression tree

    :ivar ~.operands: list of operands
    :ivar ~.evalFn: function to evaluate this operator
    :ivar ~.operator: OpDefinition instance
    :ivar ~.result: result signal of this operator
    """

    def __init__(self, operator: OpDefinition,
                 operands: Tuple[Union[RtlSignalBase, HValue]]):
        self.operands = tuple(operands)
        self.operator = operator
        self.result = None  # type: RtlSignal

    @internal
    def _replace_input(self, toReplace: RtlSignalBase, replacement: RtlSignalBase):
        new_operands = []
        for o in self.operands:
            if replace_input_in_expr(self, o, toReplace, replacement, True):
                new_operands.append(replacement)
            else:
                new_operands.append(o)
        self.operands = tuple(new_operands)

    @internal
    def staticEval(self):
        """
        Recursively statistically evaluate result of this operator
        """
        for o in self.operands:
            o.staticEval()
        self.result._val = self.evalFn()

    @internal
    def evalFn(self, simulator=None):
        """
        Syntax sugar
        """
        return self.operator.eval(self, simulator=simulator)

    @internal
    def _walk_sensitivity(self, casualSensitivity: set, seen: set, ctx: SensitivityCtx):
        seen.add(self)

        if isEventDependentOp(self.operator):
            if ctx.contains_ev_dependency:
                assert self in ctx, "has to have only one clock one clock"
            ctx.contains_ev_dependency = True
            ctx.append(self)
        else:
            # walk source of signal
            for operand in self.operands:
                if operand not in seen:
                    operand._walk_sensitivity(casualSensitivity, seen, ctx)

    @internal
    def _walk_public_drivers(self, seen: set) -> Generator["RtlSignal", None, None]:
        """
        Walk all non hiden signals in an expression
        """
        for op in self.operands:
            if not isinstance(op, HValue) and op not in seen:
                seen.add(op)
                yield from op._walk_public_drivers(seen)

    @internal
    def __eq__(self, other):
        return self is other or (
            type(self) is type(other) and
            self.operator == other.operator and
            self.operands == other.operands
        )

    @internal
    @staticmethod
    def withRes(opDef, operands, resT):
        """
        Create operator with result signal

        :ivar ~.resT: data type of result signal
        :ivar ~.outputs: iterable of signals which are outputs
            from this operator
        """
        # try return existing operator result
        for i, o in enumerate(operands):
            if isinstance(o, RtlSignalBase):
                if i == 0:
                    k = (opDef, i, *operands[1:])
                else:
                    k = (opDef, i, *operands[:i], *operands[i + 1:])
                try:
                    return o._usedOps[k]
                except KeyError:
                    pass

        # instanciate new Operator
        op = Operator(opDef, operands)
        out = RtlSignal(getCtxFromOps(operands), None, resT)
        out._const = arr_all(op.operands, isConst)
        out.drivers.append(op)
        out.origin = op
        op.result = out

        # Register potential signals to drivers/endpoints
        first_signal = True
        for i, o in enumerate(op.operands):
            if isinstance(o, RtlSignalBase):
                o.endpoints.append(op)
                if first_signal:
                    # register operator in _usedOps operator cache
                    if i == 0:
                        k = (opDef, i, *operands[1:])
                    else:
                        k = (opDef, i, *operands[:i], *operands[i + 1:])
                    o._usedOps[k] = out
                    o._usedOpsAlias[k] = {k, }
                    first_signal = False
            elif isinstance(o, HValue):
                pass
            else:
                raise NotImplementedError(
                    "Operator operands can be"
                    " only signal or values got:%r" % (o))

        if out._const:
            out.staticEval()
        return out

    @internal
    def __hash__(self):
        return hash((self.operator, self.operands))

    def _destroy(self):
        self.result.drivers.remove(self)
        for o in self.operands:
            if isinstance(o, RtlSignalBase):
                o.endpoints.remove(self)

        # clean all references on this operator instance from RtlSignal._usedOps operator cache
        _k = (self.operator, 0, *self.operands[1:])
        for k in self.operands[0]._usedOpsAlias[_k]:
            self.operands[0]._usedOps.pop(k)

