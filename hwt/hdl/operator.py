from typing import Generator, Union, Tuple, Optional, Set

from hwt.doc_markers import internal
from hwt.hdl.hdlObject import HdlObject
from hwt.hdl.operatorDefs import isEventDependentOp, OpDefinition
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.value import HValue
from hwt.pyUtils.arrayQuery import arr_all
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, RtlSignalBase, \
    OperatorCaheKeyType


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
        self.result: Optional[RtlSignal] = None

    @internal
    def staticEval(self):
        """
        Recursively statistically evaluate result of this operator
        """
        for o in self.operands:
            o.staticEval()
        self.result._val = self.operator.eval(self, simulator=None)

    @internal
    def _walk_sensitivity(self, casualSensitivity: Set[RtlSignal], seen: Set[RtlSignal], ctx: SensitivityCtx):
        """
        :see: :meth:`hwt.synthesizer.rtlLevel.rtlSignal.RtlSignal._walk_sensitivity`
        """
        seen.add(self)

        if isEventDependentOp(self.operator):
            if ctx.contains_ev_dependency:
                assert self in ctx, "has to have only a single clock signal"
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
        Walk all non hidden signals in an expression
        """
        for op in self.operands:
            if not isinstance(op, HValue) and op not in seen:
                seen.add(op)
                yield from op._walk_public_drivers(seen)

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
                break

        # instantiate new Operator
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
            else:
                assert isinstance(o, HValue), (
                    "Operator operands can be only signal or values got:", o)

        if out._const:
            # if this signal is constant precompute its value
            out.staticEval()

        return out

    @internal
    def _replace_input(self, inp: RtlSignal, replacement: RtlSignal):
        """
        Replace operand signal (non-recursively)
        
        :attention: costly operation because all records in operand cache for all inputs may be potentially updated
        """
        newOperands = []
        modified = False
        for op in self.operands:
            if op is inp:
                modified = True
                newOperands.append(replacement)
            else:
                newOperands.append(op)

        assert modified, self
        res = self.result
        for op in self.operands:
            if isinstance(op, RtlSignal):
                op: RtlSignal
                for k, v in tuple(op._usedOps.items()):
                    k: OperatorCaheKeyType
                    if v is res:
                        if op is inp:
                            # this operand is  originally replaced "inp" the cache key must be transfered
                            # from original operand to a new replacement
                            op._usedOps.pop(k)
                            replacement._usedOps[k] = v
                            aliases = op._usedOpsAlias.pop(k)
                            aliases.remove(k)
                            _aliases = None
                            for a in aliases:
                                _aliases = replacement._usedOpsAlias.get(a, None)
                                if _aliases is not None:
                                    break
                            if _aliases is None:
                                _aliases = {k, }
                            else:
                                _aliases.add(k)
                            replacement._usedOpsAlias[k] = _aliases
                        else:
                            # some other operand is originally replaced "inp" the cache key must be updated
                            op._usedOps.pop(k)
                            kNew = (*k[0:2], *(replacement if _op is inp else _op for _op in k[2:]))
                            op._usedOps[k] = v
                            aliases = op._usedOpsAlias.pop(k)
                            aliases.remove(k)
                            aliases.add(kNew)
                            op._usedOpsAlias[kNew] = aliases
            
        self.operands = tuple(newOperands)
        inp.endpoints.discard(self)
        replacement.endpoints.append(self)

    @internal
    def _destroy(self):
        self.result.drivers.remove(self)
        operands = self.operands
        first_op_sig = True
        for i, o in enumerate(operands):
            if isinstance(o, RtlSignalBase):
                # discard because operands may be the same signal
                o.endpoints.discard(self)
                if first_op_sig:
                    # clean all references on this operator instance from RtlSignal._usedOps operator cache
                    _k = (self.operator, i, *operands[:i], *operands[i + 1:])
                    for k in o._usedOpsAlias[_k]:
                        res = o._usedOps.pop(k)
                        assert res is self.result
                    first_op_sig = False
        self.result.origin = None
        self.result = None
        self.operands = None
        self.operator = None
