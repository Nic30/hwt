from hwt.hdlObjects.transactionPart import TransactionPart
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct
from hwt.hdlObjects.types.array import Array
from hwt.synthesizer.param import evalParam


class TransactionTemplateItem(object):
    """
    :ivar name: name of this item, like name in struct field
    :ivar dtype: dtype of this item, like dtype in struct field
    :ivar parent: if is derived from HStruct field this is instance of FrameTemplate for this HStruct else None
    :ivar children: if represents field of type HStruct this is instance of FrameTemplate else None
    :ivar bitAddr: address of this item in template, bit precise 
    :ivar bitAddrEnd: address of end of this item in template, bit precise 
    :ivar parts: list of instances of TransactionPart which specifies in which databus word
        this field will appear (requires resolveFieldPossitionsInFrame call)
    :ivar origin: object from which this item was generated from
    :attention: only fields of simple type like Bits have parts
        (HStruct have them on it's children, Array have information just about first word)
    """
    def __init__(self, name, dtype, bitAddr, bitAddrEnd, origin=None, parent=None, children=None):
        self.name = name
        self.isPadding = name is None
        self.dtype = dtype
        self.parent = None
        self.children = children
        if children is not None:
            children.parent = self

        self.bitAddr = bitAddr
        self.bitAddrEnd = bitAddrEnd
        
        self.parts = []
        self.origin = origin

    def _addFieldAsTransParts(self, parent, config, frameIndex, inStructBitAddr, inFrameBitAddr,
                              width, repetitionCnt=None):
        # discover parts in bus words
        DW = config.dataWidth
        partOffset = 0
        if repetitionCnt is None:
            repetitionCnt = 0
        _width = width

        while width != 0 and repetitionCnt > 0:
            wordIndex = inStructBitAddr // DW
            endOfWord = DW * (wordIndex + 1)
            
            widthOfPart = min(endOfWord, inStructBitAddr + width) - inStructBitAddr

            p = TransactionPart(parent, frameIndex, inStructBitAddr, inFrameBitAddr,
                                widthOfPart, DW, partOffset)
            self.parts.append(p)

            inStructBitAddr += widthOfPart
            inFrameBitAddr += widthOfPart
            width -= widthOfPart
            
            if inFrameBitAddr == config.maxFrameBitLen:
                inFrameBitAddr = 0
                frameIndex += 1
            
            if width == 0:
                repetitionCnt -= 1
                if repetitionCnt:
                    width = _width

        return inStructBitAddr, inFrameBitAddr, frameIndex

    def _translateDtype(self, config, bitAddr):
        """
        Some fields has to be internally split due data-width of bus,
        there we discover how to split field to words on bus
        and we resolve in which frame this item will be

        :note: params and return same as TransactionTemplate._translateDtype
        """
        t = self.dtype
        fieldWidth = self.dtype.bit_length()

        if self.isPadding:
            pass
        elif isinstance(t, Bits):
            # discover parts in bus words
            bitAddr = self._addFieldAsTransParts(self,
                                                 config,
                                                 bitAddr,
                                                 fieldWidth)

        elif isinstance(t, HStruct):
            for ch in self.children:
                bitAddr = ch._translateDtype(config,
                                             bitAddr)
        elif isinstance(t, Array):
            self.children._translateDtype(config,
                                          bitAddr,
                                          repetitionCnt=evalParam(t.size).val)
        else:
            raise NotImplementedError(t)

        return self.bitAddrEnd 
