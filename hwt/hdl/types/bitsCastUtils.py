from functools import reduce
from typing import Union
from hwt.hdl.types.bits import HBits


class BitWidthErr(Exception):
    """
    Wrong bit width of signal/value
    """


def fitTo_t(what: Union["HBitsRtlSignal", "HBitsConst"], where_t: HBits,
            extend: bool=True, shrink: bool=True) -> Union["HBitsRtlSignal", "HBitsConst"]:
    """
    Slice signal "what" to fit in "where"
    or
    arithmetically (for signed by MSB / unsigned, vector with 0) extend
    "what" to same width as "where"

    little-endian impl.

    :param extend: allow increasing of the signal width
    :param shrink: allow shrinking of the signal width
    """

    whatWidth = what._dtype.bit_length()
    toWidth = where_t.bit_length()
    if toWidth == whatWidth:
        return what
    elif toWidth < whatWidth:
        # slice
        if not shrink:
            raise BitWidthErr()

        return what[toWidth:]
    else:
        if not extend:
            raise BitWidthErr()

        w = toWidth - whatWidth

        if what._dtype.signed:
            # signed extension
            msb = what[whatWidth - 1]
            ext = reduce(lambda a, b: a._concat(b), [msb for _ in range(w)])
        else:
            # 0 extend
            ext = HBits(w).from_py(0)

        res = ext._concat(what)
        if where_t.signed is not None:
            return res._reinterpret_cast(where_t)
        return res


def fitTo(what: Union["HBitsRtlSignal", "HBitsConst"], where: Union["HBitsRtlSignal", "HBitsConst"],
          extend: bool=True, shrink: bool=True) -> Union["HBitsRtlSignal", "HBitsConst"]:
    return fitTo_t(what, where._dtype, extend, shrink)

