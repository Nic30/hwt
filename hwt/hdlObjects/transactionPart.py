
class TransactionPart(object):
    """
    Container for informations about parts of TransactionTemplateItem split on databus words
    """
    def __init__(self, tmpl, startOfPart, endOfPart, inFieldOffset):
        self.tmpl = tmpl
        self.isPadding = tmpl is None
        self.startOfPart = startOfPart
        self.endOfPart = endOfPart
        self.inFieldOffset = inFieldOffset
        self.parent = None

    def bit_length(self):
        return self.endOfPart - self.startOfPart

    def getBusWordBitRange(self):
        """
        :return: bit range which contains data of this part on bus data signal
        """
        offset = self.startOfPart % self.parent.wordWidth
        return (offset + self.bit_length(), offset)

    def getFieldBitRange(self):
        """
        :return: bit range which contains data of this part on interface of field
        """
        offset = self.inFieldOffset
        return (self.bit_length() + offset, offset)

    def isLastPart(self):
        return self.tmpl.bitAddrEnd == self.endOfPart

    def __repr__(self):
        return "<TransactionPart %r, startOfPart:%d, endOfPart:%d>" % (
               self.tmpl, self.startOfPart, self.endOfPart)
