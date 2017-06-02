from math import inf

from hwt.hdlObjects.transactionTemplateItem import TransactionTemplateItem
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct
from hwt.hdlObjects.typeShortcuts import vecT


class TransactionTemplate(list):
    """
    Container of informations about frames generated from HStruct
    """
    def __init__(self, *args, **kwargs):
        list.__init__(self, *args, **kwargs)
        self.parent = None

    def walkTransactionParts(self):
        for fi in self:
            t = fi.dtype
            if isinstance(t, Bits):
                yield from fi.transactionParts
            elif isinstance(t, HStruct):
                yield from fi.children.walkTransactionParts()
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

        for transactionPart in self.walkTransactionParts():
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
        dataWidth = self.busDataWidth

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

    def _discoverTransactionParts(self,
                                  dataWidth,
                                  inStructBitAddr,
                                  inFrameBitAddr,
                                  maxFrameBitLen,
                                  maxPaddingWords,
                                  pendingPaddingBits,
                                  frameIndex,
                                  trim,
                                  applyPaddingAtEnd=False):
        """
        :note: same like discoverTransactionInfos, just applyPaddingAtEnd added

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

        :param applyPaddingAtEnd: if True pendingPaddingBits will be used to create padding at the end of frame
            (if trim is True it has no effect)

        :return: tuple (actual inStructBitAddr, actual inFrameBitAddr, actual pendingPaddingBits, actualFrameIndex)

        """
        self.busDataWidth = dataWidth

        for fi in self:
            inStructBitAddr, inFrameBitAddr, pendingPaddingBits, frameIndex = \
            fi._discoverTransactionParts(dataWidth,
                                         inStructBitAddr,
                                         inFrameBitAddr,
                                         maxFrameBitLen,
                                         maxPaddingWords,
                                         pendingPaddingBits,
                                         frameIndex,
                                         trim)

        _pendingPaddingBits = pendingPaddingBits
        if applyPaddingAtEnd:
            aligin = dataWidth - (inStructBitAddr % dataWidth)
            if aligin and aligin != dataWidth:
                _pendingPaddingBits += aligin

        if _pendingPaddingBits:
            inStructBitAddr -= pendingPaddingBits
            inFrameBitAddr -= pendingPaddingBits
            t = vecT(_pendingPaddingBits)
            ti = TransactionTemplateItem(None, t, inFrameBitAddr, origin=None, parent=self)
            self.append(ti)
            return ti._addField(None,
                                dataWidth,
                                frameIndex,
                                inStructBitAddr,
                                inFrameBitAddr,
                                _pendingPaddingBits)

        return inStructBitAddr, inFrameBitAddr, pendingPaddingBits, frameIndex

    def discoverTransactionInfos(self,
                                 dataWidth,
                                 inStructBitAddr=0,
                                 inFrameBitAddr=0,
                                 maxFrameBitLen=inf,
                                 maxPaddingWords=inf,
                                 pendingPaddingBits=0,
                                 frameIndex=0,
                                 trim=False):
        """
        Resolve in which words field appears

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
        assert isinstance(dataWidth, int), dataWidth
        return self._discoverTransactionParts(dataWidth,
                                              inStructBitAddr,
                                              inFrameBitAddr,
                                              maxFrameBitLen,
                                              maxPaddingWords,
                                              pendingPaddingBits,
                                              frameIndex,
                                              trim,
                                              applyPaddingAtEnd=True)

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
        for tp in reversed(transactionParts):
            percentOfWidth = tp.width / self.busDataWidth
            # -1 for ending |
            fieldWidth = max(0, int(percentOfWidth * width) - 1)
            assert fieldWidth >= 0

            # percentOffset = (tp.inFrameBitAddr % self.busDataWidth) / self.busDataWidth
            # offset = int(percentOffset * width)
            name = self.__repr__getName(tp, fieldWidth)
            buff.append('{0: ^{fieldWidth}}|'.format(name, fieldWidth=fieldWidth))

        return "".join(buff)

    def __repr__(self, scale=1):
        buff = []
        padding = 5
        width = int(self.busDataWidth * scale)

        buff.append('{0: <{padding}}{1: <{halfLineWidth}}{2: >{halfLineWidth}}'.format(
            "", self.busDataWidth - 1, 0, padding=padding, halfLineWidth=width // 2))
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
