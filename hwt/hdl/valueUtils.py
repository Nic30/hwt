from typing import Union, List

from hwt.hdl.value import HValue


def isSameHVal(a: HValue, b: HValue) -> bool:
    """
    :return: True if two Value instances are same
    :note: not just equal
    """
    return a is b or (isinstance(a, HValue)
                      and isinstance(b, HValue)
                      and a.val == b.val
                      and a.vld_mask == b.vld_mask)


def areSameHVals(a: Union[None, List[HValue]],
                 b: Union[None, List[HValue]]) -> bool:
    """
    :return: True if two vectors of HValue/RtlSignal instances are same
    :note: not just equal
    """
    if a is b:
        return True
    if a is None or b is None:
        return False
    if len(a) == len(b):
        for a_, b_ in zip(a, b):
            if not isSameHVal(a_, b_):
                return False
        return True
    else:
        return False
