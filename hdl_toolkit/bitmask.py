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

    @staticmethod   
    def select(val, bitNo):
        """
        select bit from integer
        """
        
        return (val >> bitNo) & 1
    
    @staticmethod
    def selectRange(val, bitsStart, bitsLen):
        val >>= bitsStart
        return val & Bitmask.mask(bitsLen)
    
    @staticmethod
    def clean(val, bitNo):
        return val & ~(1 << bitNo)
    
    @staticmethod
    def set(val, bitNo):
        return val | (1 << bitNo)
    
    @staticmethod
    def toogle(val, bitNo):
        return val ^ (1 << bitNo)
    
    @staticmethod
    def setBitRange(val, bitStart, bitsLen, newBits):
        mask = Bitmask.mask(bitsLen)
        newBits &= mask
        
        mask <<= bitStart
        newBits <<= bitStart
        
        return (val & ~mask) | newBits
    
    @staticmethod
    def bitSetTo(val, bitNo, bitVal):
        if bitVal == 0:
            return Bitmask.clean(val, bitNo)
        elif bitVal == 1:
            return Bitmask.set(val, bitNo)
        else:
            raise NotImplementedError()
