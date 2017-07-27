from hwt.code import Concat
from hwt.synthesizer.vectorUtils import iterBits


def reverseByteOrder(signalOrVal):
    """
    Reverse byteorder (littleendian/bigendian) of signal or value
    """
    w = signalOrVal._dtype.bit_length()
    i = w
    items = []

    while i > 0:
        # take last 8 bytes or rest
        lower = max(i - 8, 0)
        items.append(signalOrVal[i:lower])
        i -= 8

    return Concat(*items)


def reversedBits(sigOrVal):
    return Concat(* list(iterBits(sigOrVal)))
