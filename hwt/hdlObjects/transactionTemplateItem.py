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
    :ivar parts: list of instances of TransactionPart which specifies in which databus word
        this field will appear (requires resolveFieldPossitionsInFrame call)
    :ivar origin: object from which this item was generated from
    :attention: only fields of simple type like Bits have parts
        (HStruct have them on it's children, Array have information just about first word)
    """
    def __init__(self, name, dtype, inFrameBitOffset, origin=None, parent=None, children=None):
        self.name = name
        self.isPadding = name is None
        self.dtype = dtype
        self.parent = None
        self.children = children
        if children is not None:
            children.parent = self

        self.inFrameBitOffset = inFrameBitOffset
        if isinstance(dtype, Bits):
            self.parts = []
        self.origin = origin

    def _addFieldAsTransParts(self, parent, dataWidth, frameIndex, inStructBitAddr, inFrameBitAddr, fieldWidth):
        # discover parts in bus words
        partOffset = 0
        while fieldWidth != 0:
            wordIndex = inStructBitAddr // dataWidth
            endOfWord = dataWidth * (wordIndex + 1)
            widthOfPart = min(endOfWord, inStructBitAddr + fieldWidth) - inStructBitAddr

            p = TransactionPart(parent, frameIndex, inStructBitAddr, inFrameBitAddr,
                                widthOfPart, dataWidth, partOffset)
            self.parts.append(p)

            inStructBitAddr += widthOfPart
            inFrameBitAddr += widthOfPart
            fieldWidth -= widthOfPart
            # [TODO] increment frame number if needed

        return inStructBitAddr, inFrameBitAddr, frameIndex

    def _translateHStruct(self,
                          config,
                          inStructBitAddr,
                          inFrameBitAddr,
                          pendingPaddingBits,
                          frameIndex):
        """
        Some fields has to be internally split due data-width of bus,
        there we discover how to split field to words on bus
        and we resolve in which frame this item will be

        :note: params and return same as TransactionTemplate._translateHStruct
        """
        DW = config.dataWidth
        assert (inStructBitAddr % DW) == (inFrameBitAddr % DW), "Only padding words can be discarded, offset should be same ins HStruct and in frame"

        t = self.dtype
        if isinstance(t, Bits):
            fieldWidth = self.dtype.bit_length()
            if self.isPadding:
                # [TODO] padding to next boundary of word
                # [TODO] increment frame number if needed
                # [TODO] trim
                pendingPaddingBits += fieldWidth
                # stag padding
                inStructBitAddr += fieldWidth
                inFrameBitAddr += fieldWidth
            else:
                if pendingPaddingBits:
                            (inStructBitAddr, inFrameBitAddr,
                             frameIndex, pendingPaddingBits) = config.mkPaddingFn(
                                                                        config,
                                                                        False,
                                                                        inStructBitAddr,
                                                                        inFrameBitAddr,
                                                                        frameIndex,
                                                                        pendingPaddingBits)

                # discover parts in bus words
                inStructBitAddr, inFrameBitAddr, frameIndex = \
                    self._addField(self,
                                   DW,
                                   frameIndex,
                                   inStructBitAddr,
                                   inFrameBitAddr,
                                   fieldWidth)

        elif isinstance(t, HStruct):
            for ch in self.children:
                (inStructBitAddr, inFrameBitAddr,
                 pendingPaddingBits, frameIndex) = ch._translateHStruct(
                                                                config,
                                                                inStructBitAddr,
                                                                inFrameBitAddr,
                                                                pendingPaddingBits,
                                                                frameIndex)
        else:
            raise NotImplementedError(t)

        return inStructBitAddr, inFrameBitAddr, pendingPaddingBits, frameIndex
