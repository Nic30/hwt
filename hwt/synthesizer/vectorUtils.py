import math

from hwt.hdlObjects.typeShortcuts import vec
from hwt.hdlObjects.types.array import HArray
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct
from hwt.hdlObjects.types.structUtils import walkFlattenFields


def fitTo(what, to):
    """
    Slice signal "what" to fit in "to"
    or
    extend "what" with zeros to same width as "to"

    little-endian impl.
    """

    whatWidth = what._dtype.bit_length()
    toWidth = to._dtype.bit_length()
    if toWidth == whatWidth:
        return what
    elif toWidth < whatWidth:
        # slice
        return what[toWidth:]
    else:
        if what._dtype.signed:
            raise NotImplementedError("Signed extension")
        # extend
        return vec(0, toWidth - whatWidth)._concat(what)


def iterBits(sigOrVal, bitsInOne=1, skipPadding=True, fillup=False):
    """
    Iterate over bits in vector

    :param sig: signal or value to iterate over
    :param bitsInOne: number of bits in one part
    :param skipPadding: if true padding is skipped in dense types
    """
    if isinstance(bitsInOne, int):
        bitsInOne = int(bitsInOne)

    t = sigOrVal._dtype
    if isinstance(t, (HStruct, HArray)):
        actual = None
        actualOffset = 0

        for f in walkFlattenFields(sigOrVal, skipPadding=skipPadding):
            thisFieldLen = f._dtype.bit_length()

            if actual is None:
                actual = f
                actuallyHave = thisFieldLen
            else:
                bitsInActual = actual._dtype.bit_length() - actualOffset
                actuallyHave = bitsInActual + thisFieldLen
                if actuallyHave >= bitsInOne:
                    # consume what was remained in actual
                    takeFromThis = bitsInOne - bitsInActual
                    yield f[takeFromThis:]._concat(actual[:actualOffset])
                    actualOffset = takeFromThis
                    actuallyHave -= bitsInOne
                    if actuallyHave > 0:
                        actual = f
                    else:
                        actual = None
                else:
                    # concat to actual because it is not enough
                    actual = f._concat(actual)

            while actuallyHave >= bitsInOne:
                yield actual[(actualOffset + bitsInOne):actualOffset]
                # update slice out what was taken
                actuallyHave -= bitsInOne
                actualOffset += bitsInOne

            if actuallyHave == 0:
                actual = None
                actualOffset = 0

        if actual is not None and fillup:
            fillupW = bitsInOne - actuallyHave
            t = f._dtype
            padding = Bits(fillupW, signed=t.signed, negated=t.negated).fromPy(None)
            yield padding._concat(actual[:actualOffset])
        else:
            assert actual is None, "Width of object has to be divisible by bitsInOne"
    else:
        w = sigOrVal._dtype.bit_length()
        if bitsInOne == 1:
            for bit in range(w):
                yield sigOrVal[bit]
        else:
            items = math.ceil(w / bitsInOne)
            for i in range(items):
                h = min(bitsInOne * (i + 1), w)
                l = bitsInOne * i
                s = sigOrVal[h:l]
                if i < items - 1 or s._dtype.bit_length() == bitsInOne:
                    yield s
                else:
                    # is last and is not complete
                    assert fillup
                    _w = s._dtype.bit_length()
                    padding = Bits(bitsInOne - _w).fromPy(None)
                    yield padding._concat(s)
