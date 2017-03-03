def mask(bits):
    return (1 << bits) - 1


def bitField(_from, to):
    """
    _from 0 to 1 -> '1'
    """
    w = to - _from
    return mask(w) << _from


def extendWithSet(mask, actualWidth, toWidth):
    return bitField(actualWidth - 1, toWidth) | mask


def selectBit(val, bitNo):
    """
    select bit from integer
    """
    return (val >> bitNo) & 1


def selectBitRange(val, bitsStart, bitsLen):
    val >>= bitsStart
    return val & mask(bitsLen)


def clean(val, bitNo):
    return val & ~(1 << bitNo)


def setBit(val, bitNo):
    return val | (1 << bitNo)


def toogle(val, bitNo):
    return val ^ (1 << bitNo)


def setBitRange(val, bitStart, bitsLen, newBits):
    _mask = mask(bitsLen)
    newBits &= _mask

    _mask <<= bitStart
    newBits <<= bitStart

    return (val & ~_mask) | newBits


def bitSetTo(val, bitNo, bitVal):
    if bitVal == 0:
        return clean(val, bitNo)
    elif bitVal == 1:
        return setBit(val, bitNo)
    else:
        raise NotImplementedError()


def align(val, lowerBitCntToAlign):
    val = val >> lowerBitCntToAlign
    return val << lowerBitCntToAlign
