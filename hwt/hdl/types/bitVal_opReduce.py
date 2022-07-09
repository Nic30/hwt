from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyMathBitPrecise.bit_utils import mask


@internal
def tryReduceAnd(sig:RtlSignalBase, val: HValue):
    """
    Return sig and val reduced by & operator or None
    if it is not possible to statically reduce expression
    """
    m = sig._dtype.all_mask()
    if val._is_full_valid():
        v = val.val
        if v == m:
            return sig
        elif v == 0:
            return val


@internal
def tryReduceOr(sig:RtlSignalBase, val: HValue):
    """
    Return sig and val reduced by | operator or None
    if it is not possible to statically reduce expression
    """
    m = sig._dtype.all_mask()
    if not val.vld_mask:
        return val

    if val._is_full_valid():
        v = val.val
        if v == m:
            return val
        elif v == 0:
            return sig


@internal
def tryReduceXor(sig:RtlSignalBase, val: HValue):
    """
    Return sig and val reduced by ^ operator or None
    if it is not possible to statically reduce expression
    """
    m = sig._dtype.all_mask()
    if not val.vld_mask:
        return val

    if val._is_full_valid():
        v = val.val
        if v == m:
            return ~sig
        elif v == 0:
            return sig


def reduceSigCheckFnAnd(op0Original:RtlSignalBase, op0Negated: bool, op1Negated:bool) -> Union[RtlSignalBase, HValue]:
    if op0Negated == op1Negated:
        # a & a -> a
        # ~a & ~a -> ~a
        return op0Original
    else:
        # a | ~a -> 0
        # ~a | a -> 0
        return op0Original._dtype.from_py(0)


def reduceSigCheckFnOr(op0Original:RtlSignalBase, op0Negated: bool, op1Negated:bool) -> Union[RtlSignalBase, HValue]:
    if op0Negated == op1Negated:
        # a | a -> a
        # ~a | ~a -> ~a
        return op0Original
    else:
        # a | ~a -> 1
        # ~a | a -> 1
        t = op0Original._dtype
        return t.from_py(mask(t.bit_length()))


def reduceSigCheckFnXor(op0Original:RtlSignalBase, op0Negated: bool, op1Negated:bool) -> Union[RtlSignalBase, HValue]:
    t = op0Original._dtype
    if op0Negated == op1Negated:
        # a ^ a -> 0
        # ~a ^ ~a -> 0
        return t.from_py(0)
    else:
        # a ^ ~a -> 1
        # ~a ^ a -> 1
        return t.from_py(mask(t.bit_length()))

