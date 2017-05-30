from hwt.hdlObjects.transactionPart import TransactionPart
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct


class TransactionTemplateItem(object):
    """
    :ivar name: name of this item, like name in struct field
    :ivar dtype: dtype of this item, like dtype in struct field
    :ivar parent: if is derived from HStruct field this is instance of FrameTemplate for this HStruct else None
    :ivar children: if represents field of type HStruct this is instance of FrameTemplate else None
    :ivar inFrameBitOffset: number of bits before start of this item in frame
    :ivar transactionParts: list of instances of TransactionPart which specifies in which databus word 
        this field will appear (requires resolveFieldPossitionsInFrame call)
    :ivar origin: object from which this item was generated from
    :attention: only fields of simple type like Bits have transactionParts 
        (HStruct have them on it's children, Array have information just about first word)
    """
    def __init__(self, name, dtype, inFrameBitOffset, origin=None, parent=None, children=None):
        self.name = name
        self.dtype = dtype
        self.parent = None
        self.children = children
        if children is not None:
            children.parent = self

        self.inFrameBitOffset = inFrameBitOffset
        if isinstance(dtype, Bits):
            self.transactionParts = []
        self.origin = origin

    def _addField(self, parent, dataWidth, frameIndex, inStructBitAddr, inFrameBitAddr, fieldWidth):
        # discover parts in bus words
        partOffset = 0
        while fieldWidth != 0:
            wordIndex = inStructBitAddr // dataWidth
            endOfWord = dataWidth * (wordIndex + 1)
            widthOfPart = min(endOfWord, inStructBitAddr + fieldWidth) - inStructBitAddr
        
            p = TransactionPart(parent, frameIndex, inStructBitAddr, inFrameBitAddr,
                                widthOfPart, dataWidth, partOffset)
            self.transactionParts.append(p)
        
            inStructBitAddr += widthOfPart
            inFrameBitAddr += widthOfPart
            fieldWidth -= widthOfPart
            # [TODO] increment frame number if needed
        
        return inStructBitAddr, inFrameBitAddr, frameIndex

    def _discoverTransactionInfos(self,
                                  dataWidth,
                                  inStructBitAddr,
                                  inFrameBitAddr,
                                  maxFrameBitLen,
                                  maxPaddingWords,
                                  pendingPaddingBits,
                                  frameIndex,
                                  trim):
        """
        Some fields has to be internally split due data-width of bus,
        there we discover how to split field to words on bus 
        and we resolve in which frame this item will be

        :note: params same as TransactionTemplate._discoverTransactionInfos
        
        :param dataWidth: width of data signal of interface for which is template builded
        :param inStructBitAddr: base bit address of this in original HStruct
        :param inFrameBitAddr: base bit address of this in actual frame
        :param maxFrameBitLen: maximum length of frame in bits
        :note: initial padding is part of frame len
        :param maxPaddingWords: threshold for maximum length of padding word sequence, if is exceeded
            dummy words are cut off and rest of fields is in next frame 
        :param pendingPaddingBits: number of padding bits before this item
        :param frameIndex: index of actual frame
        :param trim: remove padding words from start and end of frame
        
        :return: tuple (actual inStructBitAddr, actual inFrameBitAddr, actual pendingPaddingBits, actualFrameIndex)

        """
        assert (inStructBitAddr % dataWidth) == (inFrameBitAddr % dataWidth), "Only padding words can be discarded, offset should be same ins HStruct and in frame"
        
        t = self.dtype
        if isinstance(t, Bits):
            fieldWidth = self.dtype.bit_length()
            isPadding = self.name is None
            if isPadding:
                # [TODO] padding to next boundary of word
                # [TODO] increment frame number if needed
                # [TODO] trim
                pendingPaddingBits += fieldWidth
                endOfFrameWithPadding = inFrameBitAddr + pendingPaddingBits
                if endOfFrameWithPadding >= maxFrameBitLen:
                    if trim:
                        # trim padding words from end of frame
                        raise NotImplementedError()
                    else:
                        # instantiate padding if not bigger than maxPaddingWords
                        raise NotImplementedError()
                        
                # stag padding
                inStructBitAddr += fieldWidth
                inFrameBitAddr += fieldWidth
            else:
                if pendingPaddingBits:
                    isFirstNonPaddingInFrame = pendingPaddingBits == inFrameBitAddr - 1
                    paddingLargerThanWord = (pendingPaddingBits // dataWidth) > 0

                    if trim and isFirstNonPaddingInFrame and paddingLargerThanWord:
                        # trim padding words from begining of frame
                        pendingPaddingBits %= dataWidth

                    if pendingPaddingBits:
                        # add padding before
                        inStructBitAddr, inFrameBitAddr, frameIndex = \
                        self._addField(None,
                                       dataWidth,
                                       frameIndex,
                                       inStructBitAddr - pendingPaddingBits,
                                       inFrameBitAddr - pendingPaddingBits,
                                       pendingPaddingBits)
                
                        pendingPaddingBits = 0

                # discover parts in bus words
                inStructBitAddr, inFrameBitAddr, frameIndex = \
                    self._addField(self,
                                   dataWidth,
                                   frameIndex,
                                   inStructBitAddr,
                                   inFrameBitAddr,
                                   fieldWidth)
                     

        elif isinstance(t, HStruct):
            for ch in self.children:
                inStructBitAddr, inFrameBitAddr, pendingPaddingBits, frameIndex = \
                ch._discoverTransactionInfos(dataWidth,
                                  inStructBitAddr,
                                  inFrameBitAddr,
                                  maxFrameBitLen,
                                  maxPaddingWords,
                                  pendingPaddingBits,
                                  frameIndex,
                                  trim)
        else:
            raise NotImplementedError()
        
        return inStructBitAddr, inFrameBitAddr, pendingPaddingBits, frameIndex
