from copy import copy
import math
from typing import List, Union

from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.value import HValue
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from pyMathBitPrecise.bit_utils import mask


def inRange(n, start, end):
    """
    Check if n is in range <start, end)
    """
    res = (n >= start)
    if isinstance(n, (RtlSignalBase, InterfaceBase, HValue)) and\
            (not isinstance(end, int) or
             end < 2 ** n._dtype.bit_length()):
        res = res & (n < end)
    return res


def toPow2Ceil(x: int):
    """
    Get the smallest 2**N where 2**N >= x
    """
    i = 0
    while 2 ** i < x:
        i += 1
    return 2 ** i


def addressAlignBestEffort(record_width: int, bus_data_width: int):
    """
    Optionally extend the record width to be power of 2 and to consume
    smallest amount of memory possible.
    """
    if 2 * record_width <= bus_data_width:
        # multiple records in bus data word
        records_in_bus_word = math.floor(bus_data_width / record_width)
        record_width = bus_data_width // records_in_bus_word
        bus_words_in_record = 1
    else:
        # record in a 1+ bus data words
        bus_words_in_record = math.ceil(record_width / bus_data_width)
        # in order to make item indexable we need to have size which is 2**X
        bus_words_in_record = toPow2Ceil(bus_words_in_record)

        record_width = bus_data_width * bus_words_in_record
        records_in_bus_word = 1

    return record_width, records_in_bus_word, bus_words_in_record


def log2ceil(x):
    """
    Returns no of bits required to store x-1
    for example x=8 returns 3
    """

    if not isinstance(x, (int, float)):
        x = int(x)

    if x == 0 or x == 1:
        res = 1
    else:
        res = math.ceil(math.log2(x))

    return res


def isPow2(num) -> bool:
    """
    Check if number or constant is power of two
    """
    if not isinstance(num, int):
        num = int(num)
    return num != 0 and ((num & (num - 1)) == 0)


def sizeof(_type) -> int:
    "get size of type in bytes"
    s = _type.bit_length()
    return math.ceil(s / 8)


def shiftIntArray(values: List[Union[int, BitsVal]], item_width: int, shift: int):
    """
    :param values: array of values which will be shifted as a whole
    :param item_width: a bit length of a single item in array
    :param shift: specifies how many bits the array should be shifted, << is a positive shift, >> is a negative shift
    """
    if shift == 0:
        return copy(values)
    new_v = []
    t = Bits(item_width)
    if shift > 0:
        # <<
        for _ in range(shift // item_width):
            new_v.append(None)
        prev = None
        for v in values:
            if v is None and prev is None:
                _v = None
            else:
                if prev is None:
                    prev = t.from_py(None)
                if v is None:
                    v = t.from_py(None)
                elif isinstance(prev, BitsVal) and not isinstance(v, BitsVal):
                    v = t.from_py(v)
                _v = (v << shift) | (prev >> (item_width - shift))
            new_v.append(_v)
            prev = v
        if prev is None:
            v = None
        else:
            v = prev >> (item_width - shift)
        new_v.append(v)
    else:
        # shift < 0, >>
        nextIt = iter(values)
        for v in values:
            try:
                nv = next(nextIt)
            except StopIteration:
                nv = None
            if nv is None and v is None:
                _v = None
            else:
                if nv is None:
                    nv = t.from_py(None)
                if v is None:
                    v = t.from_py(None)
                _v = (v >> shift) | (nv & mask(shift))
            new_v.append(_v)

    return new_v


def hMin(a, b):
    return (a < b)._ternary(a, b)


def hMax(a, b):
    return (a > b)._ternary(a, b)
