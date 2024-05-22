from typing import Union, List

from hwt.hdl.const import HConst


def isSameHConst(a: HConst, b: HConst) -> bool:
    """
    :return: True if two Value instances are same
    :note: not just equal
    """
    return a is b or (isinstance(a, HConst)
                      and isinstance(b, HConst)
                      and a.val == b.val
                      and a.vld_mask == b.vld_mask)


def areSameHConsts(a: Union[None, List[HConst]],
                 b: Union[None, List[HConst]]) -> bool:
    """
    :return: True if two vectors of HConst/RtlSignal instances are same
    :note: not just equal
    """
    if a is b:
        return True
    if a is None or b is None:
        return False
    if len(a) == len(b):
        for a_, b_ in zip(a, b):
            if not isSameHConst(a_, b_):
                return False
        return True
    else:
        return False
