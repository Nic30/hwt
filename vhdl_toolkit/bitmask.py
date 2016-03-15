class Bitmask():
    
    @staticmethod
    def mask(bits):
        return (1 << bits) - 1
    
    @staticmethod
    def bitField(_from, to):
        """
        _from 0 to 1 -> '1'  
        """
        w = to - _from
        return Bitmask.mask(w) << _from
    
    @staticmethod
    def extendWithSet(mask, actualWidth, toWidth):    
        return Bitmask.bitField(actualWidth - 1, toWidth) | mask
