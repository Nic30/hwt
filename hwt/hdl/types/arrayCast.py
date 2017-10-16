from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import default_reinterpret_cast_fn
from hwt.synthesizer.exceptions import TypeConversionErr
from hwt.code import Concat
from hwt.hdl.types.array import HArray
from hwt.bitmask import selectBitRange, mask


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
    value = Bits(end - start, None).fromPy(None)

    while start != end:
        assert start < end, (start, end)

        dataWordIndex = start // wordWidth

        v = array[dataWordIndex]
        if reinterpretElmToType is not None:
            v = v._reinterpret_cast(reinterpretElmToType)

        endOfWord = (dataWordIndex + 1) * wordWidth
        width = min(end, endOfWord) - start
        offset = start % wordWidth

        val = selectBitRange(v.val, offset, width)
        vldMask = selectBitRange(v.vldMask, offset, width)
        updateTime = v.updateTime

        m = mask(width)
        value.val |= (val & m) << inPartOffset
        value.vldMask |= (vldMask & m) << inPartOffset
        value.updateMask = max(value.updateTime, updateTime)

        inPartOffset += width
        start += width

    return value


def reinterptet_harray_to_bits(typeFrom, sigOrVal, bitsT):
    """
    Cast HArray signal or value to signal or value of type Bits
    """
    size = int(typeFrom.size)
    widthOfElm = typeFrom.elmType.bit_length()
    w = bitsT.bit_length()
    if size * widthOfElm != w:
        raise TypeConversionErr(
            "Size of types is different", size * widthOfElm, w)

    partT = Bits(widthOfElm)
    parts = [p._reinterpret_cast(partT) for p in sigOrVal]

    return Concat(*reversed(parts))._reinterpret_cast(bitsT)


def reinterpret_harray_to_harray(typeFrom, sigOrVal, arrayT):
    mySize = int(typeFrom.size)
    myWidthOfElm = typeFrom.elmType.bit_length()
    size = int(arrayT.size)
    widthOfElm = arrayT.elmType.bit_length()

    if size * widthOfElm != mySize * myWidthOfElm:
        raise TypeConversionErr("Size of types is different",
                                size * widthOfElm, mySize * myWidthOfElm)

    if isinstance(typeFrom.elmType, Bits):
        reinterpretElmToType = None
    else:
        reinterpretElmToType = Bits(myWidthOfElm)

    res = arrayT.fromPy(None)
    for i in range(size):
        start = i * widthOfElm
        end = (i + 1) * widthOfElm
        item = getBits_from_array(
            sigOrVal, myWidthOfElm, start, end, reinterpretElmToType)
        res[i] = item._reinterpret_cast(arrayT.elmType)

    return res


def reinterpret_cast_harray(typeFrom, sigOrVal, toType):
    if isinstance(toType, Bits):
        return reinterptet_harray_to_bits(typeFrom, sigOrVal, toType)
    elif isinstance(toType, HArray):
        return reinterpret_harray_to_harray(typeFrom, sigOrVal, toType)
    else:
        return default_reinterpret_cast_fn(typeFrom, sigOrVal, toType)
