from typing import Generator, Union, Tuple, Optional, Set, Sequence

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.hdlObject import HdlObject
from hwt.hdl.operatorDefs import isEventDependentOp, HOperatorDef
from hwt.hdl.sensitivityCtx import SensitivityCtx
from hwt.hdl.types.hdlType import HdlType
from hwt.pyUtils.arrayQuery import arr_all
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, RtlSignalBase, \
    OperatorCaheKeyType


@internal
def getCtxFromOps(operands: Sequence):
    for o in operands:
        if isinstance(o, RtlSignalBase):
            return o._rtlCtx
    return None # case for casts of constants


def isConst(item: Union[HConst, RtlSignalBase]):
    """
    :return: True if expression is constant
    """
    return isinstance(item, HConst) or item._const


class HOperatorNode(HdlObject):
    """
    Class of operator in expression tree

    :ivar ~.operands: list of operands
    :ivar ~.evalFn: function to evaluate this operator
    :ivar ~.operator: HOperatorDef instance
    :ivar ~.result: result signal of this operator
    """

    def __init__(self, operator: HOperatorDef,
                 operands: Tuple[Union[RtlSignalBase, HConst]]):
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
            if not isinstance(op, HConst) and op not in seen:
                seen.add(op)
                yield from op._walk_public_drivers(seen)

    @internal
    @staticmethod
    def withRes(opDef: HOperatorDef, operands: Sequence[Union[RtlSignalBase, HConst]], resT: HdlType):
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

        # instantiate new HOperatorNode
        op = HOperatorNode(opDef, operands)
        out: RtlSignal = resT.getRtlSignalCls()(getCtxFromOps(operands), None, resT)
        out._const = arr_all(op.operands, isConst)
        out._rtlDrivers.append(op)
        out._rtlObjectOrigin = op
        op.result = out

        # Register potential signals to drivers/endpoints
        first_signal = True
        for i, o in enumerate(op.operands):
            if isinstance(o, RtlSignalBase):
                o._rtlEndpoints.append(op)
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
                assert isinstance(o, HConst), (
                    "HOperatorNode operands can be only signal or values got:", o)

        # pre-compute constant signal if all used types support it
        if out._const:
            precompute = resT._PRECOMPUTE_CONSTANT_SIGNALS
            for o in operands:
                precompute &= o._dtype._PRECOMPUTE_CONSTANT_SIGNALS
                if not precompute:
                    break

            if precompute:
                # if this signal is constant precompute its value
                out.staticEval()

        return out

    @internal
    def _replace_input(self, inp: RtlSignal, replacement: RtlSignal):
        """
        Replace operand signal (non-recursively)
        
        :attention: costly operation because all records in operand cache for all inputs may be potentially updated
        """
        assert self.result._rtlCtx is replacement._rtlCtx, self
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
                            op._usedOps[kNew] = v
                            aliases = op._usedOpsAlias.pop(k)
                            aliases.remove(k)
                            aliases.add(kNew)
                            op._usedOpsAlias[kNew] = aliases
                break  # _usedOps/_usedOpsAlias is relevant only for the first operand

        self.operands = tuple(newOperands)
        inp._rtlEndpoints.discard(self)
        replacement._rtlEndpoints.append(self)

    @internal
    def _destroy(self):
        self.result._rtlDrivers.remove(self)
        operands = self.operands
        first_op_sig = True
        for i, o in enumerate(operands):
            if isinstance(o, RtlSignalBase):
                # discard because same signal can be on multiple places in operand list
                o._rtlEndpoints.discard(self)
                if first_op_sig:
                    # clean all references on this operator instance from RtlSignal._usedOps operator cache
                    _k = (self.operator, i, *operands[:i], *operands[i + 1:])
                    for k in o._usedOpsAlias[_k]:
                        res = o._usedOps.pop(k)
                        assert res is self.result, (self.result._rtlCtx.parent, "HOperatorNode was not stored properly in operand cache", res, self.result, o)
                    first_op_sig = False
        self.result._rtlObjectOrigin = None
        self.result = None
        self.operands = None
        self.operator = None
