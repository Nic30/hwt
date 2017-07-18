from hwt.bitmask import mask
from hwt.hdlObjects.types.bits import Bits
from hwt.simulator.types.simBitsConversions import convertSimBits__val


__simBitsTCache = {}


def simBitsT(width, signed):
    """
    Construct SimBitsT with cache
    """
    k = (width, signed)
    try:
        return __simBitsTCache[k]
    except KeyError:
        t = SimBitsT(width, signed)
        __simBitsTCache[k] = t
        return t


class SimBitsT(Bits):
    """
    Simplified Bits type for simulation purposes
    """
    def __init__(self, width, signed):
        self._widthVal = width
        self.signed = signed
        self._allMask = mask(self._widthVal)

    def __eq__(self, other):
        return isinstance(other, Bits) and other._widthVal == self._widthVal\
            and self.signed == other.signed

    def __hash__(self):
        return hash((self._widthVal, self.signed))

    def convert(self, sigOrVal, toType):
        return convertSimBits__val(self, sigOrVal, toType)

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        return "<SimBitsT, signed:%r, %dbits>" % (self.signed, self._widthVal)

SIM_BIT = SimBitsT(1, None)
