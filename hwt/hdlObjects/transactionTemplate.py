from math import inf

from hwt.hdlObjects.transactionTemplateItem import TransactionTemplateItem
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct
from hwt.synthesizer.param import evalParam


class TransactionTemplateConfig():
    """
    Container of configuration for TransactionTemplate.translateHStruct

    :ivar dataWidth: width of data signal of interface for which is template builded
    :ivar mkChildFn: function which is called to instantiate children
        return tuple (inStructBitAddr, inFrameBitAddr, pendingPaddingBits, frameIndex)
    :ivar maxFrameBitLen: maximum length of frame in bits
    :ivar maxPaddingWords: threshold for maximum length of padding word sequence, if is exceeded
        dummy words are cut off and rest of fields is in next frame
    :ivar trim: remove padding words from start and end of frame
    """
    def __init__(self, dataWidth, mkChildFn=None, mkPaddingFn=None,
                 maxFrameBitLen=inf, maxPaddingWords=inf, trim=False):
        self.dataWidth = dataWidth
        if mkChildFn is None:
            self.mkChildFn = self.defaultMkChildFn
        else:
            self.mkChildFn = mkChildFn

        #if mkPaddingFn is None:
        #    self.mkPaddingFn = self.defaultMkPaddingFn
        #else:
        #    self.mkPaddingFn = mkPaddingFn
        
        self.maxFrameBitLen = maxFrameBitLen
        self.maxPaddingWords = maxPaddingWords
        self.trim = trim

    def defaultMkChildFn(self):
        raise NotImplementedError()

    def paddingBeforeItem(self):
        pass

    def paddingAfterItem(self):
        pass

    def paddingBeforeFrame(self):
        pass

    def paddingAfterFrame(self):
        pass
    
    

    #def defaultMkPaddingFn(self, config, isTop, inStructBitAddr, inFrameBitAddr,
    #                      frameIndex, pendingPaddingBits):
    #   # padding items are not created only addr space is dense
    #   # in some cases we wont to cut padding from start/end of frame or split frame when padding
    #   # is too high, this is why we need pendingPaddingBits
    #   # 
    #   # padding in HStruct
    #   # * padding od start/end of struct is merged with surrounding one
    #   # padding in Array
    #   # * start of array and size is noted in array
    #   # * used parts of element are stored in child of TransactionTemplateItem which represents this Array
    #   # * 
    #   _pendingPaddingBits = pendingPaddingBits
    #   DW = config.dataWidth
    #   # [TODO] padding to next boundary of word
    #   # [TODO] increment frame number if needed
    #   # [TODO] trim
    #
    #   if isTop:
    #       aligin = DW - (inStructBitAddr % DW)
    #       if aligin and aligin != DW:
    #           _pendingPaddingBits += aligin
    #
    #   if _pendingPaddingBits:
    #       inStructBitAddr -= pendingPaddingBits
    #       inFrameBitAddr -= pendingPaddingBits
    #       t = vecT(_pendingPaddingBits)
    #       ti = TransactionTemplateItem(None, t, inFrameBitAddr, origin=None, parent=self)
    #       self.append(ti)
    #
    #       (inStructBitAddr,
    #        inFrameBitAddr,
    #        frameIndex) = ti._addField(None,
    #                                   DW,
    #                                   frameIndex,
    #                                   inStructBitAddr,
    #                                   inFrameBitAddr,
    #                                   _pendingPaddingBits)
    #       pendingPaddingBits = 0
    #
    #   # endOfFrameWithPadding = inFrameBitAddr + pendingPaddingBits
    #   # if endOfFrameWithPadding >= config.maxFrameBitLen:
    #   #     if config.trim:
    #   #         # trim padding words from end of frame
    #   #         raise NotImplementedError()
    #   #     else:
    #   #         # instantiate padding if not bigger than maxPaddingWords
    #   #         raise NotImplementedError()
    #
    #
    #   # isFirstNonPaddingInFrame = pendingPaddingBits == inFrameBitAddr - 1
    #   # paddingLargerThanWord = (pendingPaddingBits // DW) > 0
    #   # 
    #   # if config.trim and isFirstNonPaddingInFrame and paddingLargerThanWord:
    #   #     # trim padding words from beginning of frame
    #   #     pendingPaddingBits %= DW
    #   # 
    #   # if pendingPaddingBits:
    #   #     # add padding before
    #   #     (inStructBitAddr,
    #   #      inFrameBitAddr,
    #   #      frameIndex) = self._addFieldAsTransParts(
    #   #                                None,
    #   #                                DW,
    #   #                                frameIndex,
    #   #                                inStructBitAddr - pendingPaddingBits,
    #   #                                inFrameBitAddr - pendingPaddingBits,
    #   #                                pendingPaddingBits)
    #   # 
    #   #     pendingPaddingBits = 0
    #
    #   return (inStructBitAddr, inFrameBitAddr, frameIndex, pendingPaddingBits)


class TransactionTemplate(object):
    """
    Container of informations about frames generated from any HType (HStruct etc.)
    """
    def __init__(self, dtype, bitAddr=0, parent=None, origin=None):
        """
        :ivar config: original TransactionTemplateConfig which was use to generate this template
        """
        self.parent = parent
        self.origin = origin
        self.dtype = dtype

        self.children = []
        
        self._loadFromHType(dtype, bitAddr)
        
    def walkParts(self):
        for fi in self:
            t = fi.dtype
            if isinstance(t, Bits):
                yield from fi.parts
            elif isinstance(t, HStruct):
                yield from fi.children.walkParts()
            else:
                raise NotImplementedError(t)

    def walkFrameWords(self, skipPadding=True):
        """
        Walks words in all frames

        :return: generator of tuples (wordIndex(cumulative),
            list of TransactionPart instances in this word)
        """
        wordRecord = []
        actualFrame = 0
        actualWord = 0
        wordsInPrevFrames = 0

        indx = self.wordIndxFromBitAddr

        for transactionPart in self.walkParts():
            assert transactionPart.frameIndex >= actualFrame
            isPadding = transactionPart.isPadding

            w = indx(transactionPart.inFrameBitAddr)

            if transactionPart.frameIndex > actualFrame:
                # this part is in next frame
                if wordRecord:
                    yield wordsInPrevFrames + actualWord, wordRecord
                if isPadding and skipPadding:
                    wordRecord = []
                else:
                    wordRecord = [transactionPart, ]
                wordsInPrevFrames += actualWord
                actualWord = w
                actualFrame = transactionPart.frameIndex
            elif w == actualWord:
                # this part is in this same word
                if not (isPadding and skipPadding):
                    wordRecord.append(transactionPart)
            elif w > actualWord:
                # this part is in next word
                if wordRecord:
                    yield wordsInPrevFrames + actualWord, wordRecord

                if isPadding and skipPadding:
                    wordRecord = []
                else:
                    wordRecord = [transactionPart, ]
                actualWord = w
            else:
                raise NotImplementedError("Input frame info has to be sorted")

        if wordRecord:
            yield wordsInPrevFrames + actualWord, wordRecord

    def wordIndxFromBitAddr(self, bitAddr):
        dataWidth = self.config.dataWidth
        return bitAddr // dataWidth

    def _loadFromArray(self, dtype, bitAddr):
        self.itemCnt = evalParam(dtype.size).val
        self.children = TransactionTemplate(dtype.elmType, 0, self, origin=self.origin)
        
        return self.itemCnt * self.children.bitAddrEnd
        
    def _loadFromBits(self, dtype, bitAddr):
        return bitAddr + dtype.bit_length()

    def _loadFromHType(self, dtype, bitAddr):
        self.bitAddr = bitAddr

        if isinstance(dtype, HStruct):
            ld = self._loadFromHStruct
        elif isinstance(dtype, Array):
            ld = self._loadFromArray
        else:
            ld = self._loadFromBits
        
        self.bitAddrEnd = ld(dtype, bitAddr)        
        
    def _loadFromHStruct(self, dtype, bitAddr):
        for f in dtype.fields:
            t = f.dtype
            origin = f
            isPadding = f.name is None

            if isPadding:
                width = t.bit_length()
                bitAddr += width
            else:
                fi = TransactionTemplate(t, bitAddr, parent=self, origin=origin)
                self.children.append(fi)
                bitAddr = fi.bitAddrEnd
        
        return bitAddr
    
    def _translate(self, config, inFrameBitAddr, pendingPaddingBits, frameIndex,
                        isTop=False):
        """
        :note: same like translate, just pending bits added
        :param isTop: tells if this call is on top of structure (used when you need to resolve f.e. end of transaction)

        :return: tuple (actual inFrameBitAddr, actual pendingPaddingBits, actualFrameIndex)
        """
        self.config = config

        for fi in self:
            (inFrameBitAddr,
             pendingPaddingBits,
             frameIndex) = fi._translate(config,
                                         inFrameBitAddr,
                                         pendingPaddingBits,
                                         frameIndex)

        (inFrameBitAddr,
         frameIndex,
         pendingPaddingBits) = config.mkPaddingFn(self, config, isTop,
                                                  inFrameBitAddr, frameIndex,
                                                  pendingPaddingBits)

        assert pendingPaddingBits == 0, "Should be discarded or used by mkPaddingFn"
        return (inFrameBitAddr, pendingPaddingBits, frameIndex)

    def translate(self, config, inFrameBitAddr=0, pendingPaddingBits=0, frameIndex=0):
        """
        Resolve in which words field appears, and how transaction will be divided into frames and padding

        :param config: instance of TransactionTemplateConfig
        :param inFrameBitAddr: base bit address of this in actual frame
        :note: initial padding is part of frame len
        :param frameIndex: index of actual frame

        :return: tuple (inFrameBitAddrEnd, lastFrameIndex)
        """

        assert isinstance(config, TransactionTemplateConfig), config

        (inFrameBitAddr,
         _, frameIndex) = self._translateDtype(config,
                                              inFrameBitAddr,
                                              pendingPaddingBits,
                                              frameIndex,
                                              isTop=True)

        return (inFrameBitAddr, frameIndex)

    def __repr__getName(self, transactionPart, fieldWidth):
        names = []
        tp = transactionPart
        while tp is not None:
            if isinstance(tp, TransactionTemplateItem):
                name = tp.name
                names.append(name)
            tp = tp.parent

        if not names:
            return "X"*fieldWidth
        else:
            return ".".join(reversed(names))

    def __repr__word(self, index, width, padding, transactionParts):
        buff = ["{0: <{padding}}|".format(index, padding=padding)]
        DW = self.config.dataWidth

        for tp in reversed(transactionParts):
            percentOfWidth = tp.width / DW
            # -1 for ending |
            fieldWidth = max(0, int(percentOfWidth * width) - 1)
            assert fieldWidth >= 0

            # percentOffset = (tp.inFrameBitAddr % DW) / DW
            # offset = int(percentOffset * width)
            name = self.__repr__getName(tp, fieldWidth)
            buff.append('{0: ^{fieldWidth}}|'.format(name, fieldWidth=fieldWidth))

        return "".join(buff)

    def __repr__(self, scale=1):
        buff = []
        padding = 5
        DW = self.config.dataWidth
        width = int(DW * scale)

        buff.append('{0: <{padding}}{1: <{halfLineWidth}}{2: >{halfLineWidth}}'.format(
            "", DW - 1, 0, padding=padding, halfLineWidth=width // 2))
        line = '{0: <{padding}}{1:-<{lineWidth}}'.format(
            "", "", padding=padding, lineWidth=width + 1)
        buff.append(line)

        lastW = -1
        lastFrame = 0
        for w, transactionParts in self.walkFrameWords(skipPadding=False):
            while lastW + 1 < w:
                # draw padding words
                lastW += 1
                buff.append(self.__repr__word(lastW, width, padding, []))

            if transactionParts[0].frameIndex != lastFrame:
                # space between frames
                buff.append("")

            buff.append(self.__repr__word(w, width, padding, transactionParts))
            lastW = w
            lastFrame = transactionParts[0].frameIndex

        buff.append(line)

        return "\n".join(buff)
