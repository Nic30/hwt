from math import inf

from hwt.hdlObjects.transactionTemplateItem import TransactionTemplateItem
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct
from hwt.hdlObjects.typeShortcuts import vecT


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
    def __init__(self, dataWidth, mkChildFn, mkPaddingFn, maxFrameBitLen=inf, maxPaddingWords=inf, trim=False):
        self.dataWidth = dataWidth
        self.mkChildFn = mkChildFn
        self.mkPaddingFn = mkPaddingFn
        self.maxFrameBitLen = maxFrameBitLen
        self.maxPaddingWords = maxPaddingWords
        self.trim = trim

    def defaultMkChildFn(self):
        raise NotImplementedError()

    def defaultMkPaddingFn(self, config, isTop, inStructBitAddr, inFrameBitAddr,
                           frameIndex, pendingPaddingBits):
        _pendingPaddingBits = pendingPaddingBits
        DW = config.dataWidth

        if isTop:
            aligin = DW - (inStructBitAddr % DW)
            if aligin and aligin != DW:
                _pendingPaddingBits += aligin

        if _pendingPaddingBits:
            inStructBitAddr -= pendingPaddingBits
            inFrameBitAddr -= pendingPaddingBits
            t = vecT(_pendingPaddingBits)
            ti = TransactionTemplateItem(None, t, inFrameBitAddr, origin=None, parent=self)
            self.append(ti)

            (inStructBitAddr,
             inFrameBitAddr,
             frameIndex) = ti._addField(None,
                                        DW,
                                        frameIndex,
                                        inStructBitAddr,
                                        inFrameBitAddr,
                                        _pendingPaddingBits)
            pendingPaddingBits = 0

        # endOfFrameWithPadding = inFrameBitAddr + pendingPaddingBits
        # if endOfFrameWithPadding >= config.maxFrameBitLen:
        #     if config.trim:
        #         # trim padding words from end of frame
        #         raise NotImplementedError()
        #     else:
        #         # instantiate padding if not bigger than maxPaddingWords
        #         raise NotImplementedError()


        # isFirstNonPaddingInFrame = pendingPaddingBits == inFrameBitAddr - 1
        # paddingLargerThanWord = (pendingPaddingBits // DW) > 0
        # 
        # if config.trim and isFirstNonPaddingInFrame and paddingLargerThanWord:
        #     # trim padding words from beginning of frame
        #     pendingPaddingBits %= DW
        # 
        # if pendingPaddingBits:
        #     # add padding before
        #     (inStructBitAddr,
        #      inFrameBitAddr,
        #      frameIndex) = self._addFieldAsTransParts(
        #                                None,
        #                                DW,
        #                                frameIndex,
        #                                inStructBitAddr - pendingPaddingBits,
        #                                inFrameBitAddr - pendingPaddingBits,
        #                                pendingPaddingBits)
        # 
        #     pendingPaddingBits = 0

        return (inStructBitAddr, inFrameBitAddr, frameIndex, pendingPaddingBits)


class TransactionTemplate(list):
    """
    Container of informations about frames generated from HStruct
    """
    def __init__(self, *args, **kwargs):
        """
        :ivar config: original TransactionTemplateConfig which was use to generate this template
        """

        list.__init__(self, *args, **kwargs)
        self.parent = None
        self.config = None

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

    @classmethod
    def _fromHStruct(cls, structT, inFrameOffset):
        for f in structT.fields:
            t = f.dtype
            origin = f
            isPadding = f.name is None

            if isPadding:
                # do not care about structure when it is only padding, replace it with Bits of same size
                origin = None
                t = vecT(t.bit_length())
                children = None
            elif isinstance(t, HStruct):
                children = cls(cls._fromHStruct(t, inFrameOffset))
                for chch in children:
                    chch.parent = children
            else:
                children = None

            fi = TransactionTemplateItem(f.name, t, inFrameOffset, children=children, origin=origin)
            yield fi

            inFrameOffset += t.bit_length()

    @classmethod
    def fromHStruct(cls, structT):
        self = cls(cls._fromHStruct(structT, 0))
        for fi in self:
            fi.parent = self

        return self

    def _translateHStruct(self,
                          config,
                          inStructBitAddr,
                          inFrameBitAddr,
                          pendingPaddingBits,
                          frameIndex,
                          isTop=False):
        """
        :note: same like translateHStruct, just pending bits added
        :param pendingPaddingBits: number of padding bits before this item
        :param isTop: tells if this call is on top of structure (used when you need to resolve f.e. end of transaction)

        :return: tuple (actual inStructBitAddr, actual inFrameBitAddr, actual pendingPaddingBits, actualFrameIndex)
        """
        self.config = config

        for fi in self:
            (inStructBitAddr, inFrameBitAddr,
             pendingPaddingBits, frameIndex) = fi._translateHStruct(config,
                                                                    inStructBitAddr,
                                                                    inFrameBitAddr,
                                                                    pendingPaddingBits,
                                                                    frameIndex)

        (inStructBitAddr, inFrameBitAddr,
         frameIndex, pendingPaddingBits) = config.mkPaddingFn(config, isTop, inStructBitAddr,
                                                              inFrameBitAddr, frameIndex,
                                                              pendingPaddingBits)
        assert pendingPaddingBits == 0
        return (inStructBitAddr, inFrameBitAddr, pendingPaddingBits, frameIndex)

    def translateHStruct(self,
                         config,
                         inStructBitAddr=0,
                         inFrameBitAddr=0,
                         pendingPaddingBits=0,
                         frameIndex=0):
        """
        Resolve in which words field appears

        :param config: instance of TransactionTemplateConfig
        :param inStructBitAddr: base bit address of this in original HStruct
        :param inFrameBitAddr: base bit address of this in actual frame
        :note: initial padding is part of frame len
        :param frameIndex: index of actual frame

        :return: tuple (actual inStructBitAddr, actual inFrameBitAddr, actual pendingPaddingBits, actualFrameIndex)
        """

        assert isinstance(config, TransactionTemplateConfig), config
        (inStructBitAddr, inFrameBitAddr,
         _, frameIndex) = self._translateHStruct(config,
                                                 inStructBitAddr,
                                                 inFrameBitAddr,
                                                 pendingPaddingBits,
                                                 frameIndex,
                                                 isTop=True)

        return (inStructBitAddr, inFrameBitAddr, frameIndex)

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
