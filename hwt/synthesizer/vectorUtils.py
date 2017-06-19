from hwt.hdlObjects.typeShortcuts import vec
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BIT


def aplyIndexOnSignal(sig, dstType, index):
    if sig._dtype == BIT or dstType == BIT:
        return sig[index]
    elif isinstance(dstType, Bits):
        w = dstType.width
        return sig[(w * (index + 1)):(w * index)]
    else:
        raise NotImplementedError()


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
        # extend
        return vec(0, toWidth - whatWidth)._concat(what)
