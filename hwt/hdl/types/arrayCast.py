from hwt.code import Concat
from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import default_reinterpret_cast_fn
from hwt.synthesizer.exceptions import TypeConversionErr
from pyMathBitPrecise.bit_utils import get_bit_range, mask
from hwt.hdl.types.struct import HStruct


@internal
def getBits_from_array(array, wordWidth, start, end,
                       reinterpretElmToType=None):
    """
    Gets value of bits between selected range from memory

    :param start: bit address of start of bit of bits
    :param end: bit address of first bit behind bits
    :return: instance of BitsVal (derived from SimBits type) which contains
        copy of selected bits
    """
    inPartOffset = 0
    value = Bits(end - start, None).from_py(None)

    while start != end:
        assert start < end, (start, end)

        dataWordIndex = start // wordWidth

        v = array[dataWordIndex]
        if reinterpretElmToType is not None:
            v = v._reinterpret_cast(reinterpretElmToType)

        endOfWord = (dataWordIndex + 1) * wordWidth
        width = min(end, endOfWord) - start
        offset = start % wordWidth

        val = get_bit_range(v.val, offset, width)
        vld_mask = get_bit_range(v.vld_mask, offset, width)

        m = mask(width)
        value.val |= (val & m) << inPartOffset
        value.vld_mask |= (vld_mask & m) << inPartOffset

        inPartOffset += width
        start += width

    return value


@internal
def reinterptet_harray_to_bits(typeFrom, sigOrVal, bitsT):
    """
    Cast HArray signal or value to signal or value of type Bits
    """
    size = int(typeFrom.size)
    widthOfElm = typeFrom.element_t.bit_length()
    w = bitsT.bit_length()
    if size * widthOfElm != w:
        raise TypeConversionErr(
            "Size of types is different", size * widthOfElm, w)

    partT = Bits(widthOfElm)
    parts = [p._reinterpret_cast(partT) for p in sigOrVal]

    return Concat(*reversed(parts))._reinterpret_cast(bitsT)


@internal
def reinterpret_harray_to_harray(typeFrom, sigOrVal, arrayT):
    mySize = int(typeFrom.size)
    myWidthOfElm = typeFrom.element_t.bit_length()
    size = int(arrayT.size)
    widthOfElm = arrayT.element_t.bit_length()

    if size * widthOfElm != mySize * myWidthOfElm:
        raise TypeConversionErr("Size of types is different",
                                size * widthOfElm, mySize * myWidthOfElm)

    if isinstance(typeFrom.element_t, Bits):
        reinterpretElmToType = None
    else:
        reinterpretElmToType = Bits(myWidthOfElm)

    res = arrayT.from_py(None)
    for i in range(size):
        start = i * widthOfElm
        end = (i + 1) * widthOfElm
        item = getBits_from_array(
            sigOrVal, myWidthOfElm, start, end, reinterpretElmToType)
        res[i] = item._reinterpret_cast(arrayT.element_t)

    return res


@internal
def reinterpret_harray_to_hstruct(typeFrom, sigOrVal, structT):
    as_bits = sigOrVal._reinterpret_cast(Bits(typeFrom.bit_length()))
    return as_bits._reinterpret_cast(structT)


@internal
def reinterpret_cast_harray(typeFrom, sigOrVal, toType):
    if isinstance(toType, Bits):
        return reinterptet_harray_to_bits(typeFrom, sigOrVal, toType)
    elif isinstance(toType, HArray):
        return reinterpret_harray_to_harray(typeFrom, sigOrVal, toType)
    elif isinstance(toType, HStruct):
        return reinterpret_harray_to_hstruct(typeFrom, sigOrVal, toType)
    else:
        return default_reinterpret_cast_fn(typeFrom, sigOrVal, toType)
