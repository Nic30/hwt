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
    def __init__(self, widthConstr, signed):
        self.constrain = widthConstr
        self.signed = signed
        self._allMask = mask(self.bit_length())
    
    def __eq__(self, other):
        return isinstance(other, Bits) and other.bit_length() == self.bit_length()\
            and self.signed == other.signed
    
    def __hash__(self):
        return hash((self.constrain, self.signed))
    
    def all_mask(self):
        return self._allMask
    
    def bit_length(self):
        return self.constrain

    def convert(self, sigOrVal, toType):
        return convertSimBits__val(self, sigOrVal, toType)