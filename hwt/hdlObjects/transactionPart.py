class TransactionPart():
    """
    Container for informations about parts of TransactionTemplateItem split on databus words 
    """
    def __init__(self, parent, frameIndex, inStructBitAddr, inFrameBitAddr, width,
                 busDataWidth, offsetOfPart):
        """
        Container of informations about one word of transaction for one HStruct field
        
        :param parent: original TransactionTemplateItem which this part was generated from
            if is None this part is padding
        :param frameIndex: index of frame in which this part appears
        :param inStructBitAddr: base bit address of this in original HStruct
        :param inFrameBitAddr: base bit address of this field part in frame
        :param width: width of this field part
        :param busDataWidth: width of data signal for this transaction
        :param offsetOfPart: offset (bit address) of this part in original field
        
        :note: ranges in little endian notation
        
        """
        self.parent = parent
        self.frameIndex = frameIndex
        self.inStructBitAddr = inStructBitAddr
        self.inFrameBitAddr = inFrameBitAddr
        self.width = width
        self.busDataWidth = busDataWidth
        self.offsetOfPart = offsetOfPart
    
    def getBusWordBitRange(self):
        """
        :return: bit range which contains data of this part on bus data signal
        """
        offset = self.inStructBitAddr % self.busDataWidth
        return (offset + self.width, offset)
    
    def getFieldBitRange(self):
        """
        :return: bit range which contains data of this part on interface of field
        """
        offset = self.offsetOfPart
        return (self.width + offset, offset)
    
    def __repr__(self):
        return "<TransactionPart frameIndex:%d, inStructBitAddr:%d, inFrameBitAddr:%r, width:%r, offsetOfPart:%r>" % (
                self.frameIndex, self.inStructBitAddr, self.inFrameBitAddr, self.width, self.offsetOfPart)

