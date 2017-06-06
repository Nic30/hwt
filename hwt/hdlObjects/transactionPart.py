from math import inf, floor, ceil
import re

from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct


def walkFlatten(transactionTmpl, offset=None, shouldEnterFn=lambda transTmpl: True):
    """
    Walk fields in instance of TransactionTemplate
    :param shouldEnterFn: function (transTmpl) which returns True when field should
        be split on it's children
    """
    t = transactionTmpl.dtype
    base = transactionTmpl.bitAddr
    end = transactionTmpl.bitAddrEnd

    if offset is not None:
        base += offset
        end += offset

    if isinstance(t, Bits):
        yield ((base, end), transactionTmpl)
    elif isinstance(t, HStruct):
        if shouldEnterFn(transactionTmpl):
            for ch in transactionTmpl.children:
                yield from walkFlatten(ch, shouldEnterFn=shouldEnterFn)
        else:
            yield ((base, end), transactionTmpl)

    elif isinstance(t, Array):
        if shouldEnterFn(transactionTmpl):
            itemSize = (transactionTmpl.bitAddrEnd - transactionTmpl.bitAddr) // transactionTmpl.itemCnt
            for i in range(transactionTmpl.itemCnt):
                yield from walkFlatten(transactionTmpl.children,
                                       offset=base + i * itemSize,
                                       shouldEnterFn=shouldEnterFn)
        else:
            yield ((base, end), transactionTmpl)
    else:
        raise NotImplementedError(t)


class FrameTemplate(object):
    __RE_RM_ARRAY_DOTS = re.compile("(\.\[)")

    def __init__(self, dataWidth, startBitAddr, endBitAddr, transactionParts):
        self.dataWidth = dataWidth
        self.startBitAddr = startBitAddr
        self.endBitAddr = endBitAddr
        self.parts = transactionParts
        for p in self.parts:
            p.parent = self

    @staticmethod
    def framesFromTransactionTemplate(transactionTmpl,
                                      dataWidth,
                                      maxFrameLen=inf,
                                      maxPaddingWords=inf,
                                      trimPaddingWordsOnEnd=False,
                                      trimPaddingWordsOnStart=False):
        isFirstInFrame = True
        partsPending = False
        frameIndex = 0

        startOfThisFrame = 0
        endOfThisFrame = maxFrameLen
        parts = []

        for (base, end), tmpl in walkFlatten(transactionTmpl):
            startOfPart = base
            while startOfPart != end:
                if startOfPart == endOfThisFrame:
                    frameIndex += 1
                    isFirstInFrame = True
                    startOfThisFrame = endOfThisFrame
                    partsPending = False
                    yield FrameTemplate(dataWidth, startOfThisFrame, endOfThisFrame, parts)

                if isFirstInFrame:
                    partsPending = True
                    isFirstInFrame = False
                    padding = base - startOfThisFrame

                    if not trimPaddingWordsOnStart and padding > dataWidth:
                        startOfThisFrame += (padding // dataWidth) * dataWidth

                    endOfThisFrame = startOfThisFrame + maxFrameLen

                wordIndex = startOfPart // dataWidth
                endOfWord = dataWidth * (wordIndex + 1)

                endOfPart = min(endOfWord, end, endOfThisFrame)

                inFieldOffset = end - endOfPart
                p = TransactionPart(tmpl, startOfPart, endOfPart, inFieldOffset)
                parts.append(p)

                startOfPart = endOfPart

        if partsPending:
            yield FrameTemplate(dataWidth, startOfThisFrame, startOfPart, parts)

    def _wordIndx(self, addr):
        return floor(addr / self.dataWidth)
    
    def getWordCnt(self):
        return ceil((self.endBitAddr - self.startBitAddr) / self.dataWidth) 
    
    def walkWords(self, showPadding=False):
        wIndex = 0
        lastEnd = self.startBitAddr
        parts = []
        for p in self.parts:
            end = p.startOfPart
            if showPadding and end != lastEnd:
                # insert padding
                while end != lastEnd:
                    assert end >= lastEnd, (end, lastEnd)
                    endOfWord = (self._wordIndx(lastEnd) + 1) * self.dataWidth
                    endOfPadding = min(endOfWord, end)
                    _p = TransactionPart(None, lastEnd, endOfPadding, 0)
                    _p.parent = self
                    parts.append(_p)

                    if endOfPadding >= endOfWord:
                        yield (wIndex, parts)
                        wIndex += 1
                        parts = []

                    lastEnd = endOfPadding

            if self._wordIndx(lastEnd) != self._wordIndx(p.startOfPart):
                yield (wIndex, parts)

                wIndex += 1
                parts = []
                lastEnd = p.endOfPart

            parts.append(p)
            lastEnd = p.endOfPart
            if lastEnd % self.dataWidth == 0:
                yield (wIndex, parts)

                wIndex += 1
                parts = []

        if showPadding and (parts or lastEnd != self.endBitAddr or lastEnd % self.dataWidth != 0):
            end = (self._wordIndx(self.endBitAddr) + 1) * self.dataWidth
            if showPadding:
                while end != lastEnd:
                    assert end >= lastEnd, (end, lastEnd)
                    endOfWord = lastEnd + self.dataWidth
                    endOfPadding = min(endOfWord, end)
                    _p = TransactionPart(None, lastEnd, endOfPadding, 0)
                    _p.parent = self
                    parts.append(_p)

                    if endOfPadding >= endOfWord:
                        yield (wIndex, parts)
                        wIndex += 1
                        parts = []

                    lastEnd = endOfPadding

            if parts:
                yield (wIndex, parts)

    def __repr__getName(self, transactionPart, fieldWidth):
        if transactionPart.isPadding:
            return "X"*fieldWidth
        else:
            names = []
            tp = transactionPart.tmpl
            while tp is not None:
                try:
                    isArrayElm = isinstance(tp.parent.dtype, Array)
                except AttributeError:
                    isArrayElm = False

                if isArrayElm:
                    arr = transactionPart.tmpl.parent
                    arrS = arr.bitAddr
                    itemW = (arr.bitAddrEnd - arrS) // arr.itemCnt
                    s = transactionPart.startOfPart
                    indx = (s - arrS) // itemW
                    names.append("[%d]" % indx)
                else:
                    o = tp.origin
                    if o is None:
                        break
                    if o.name is not None:
                        names.append(o.name)
                tp = tp.parent

            # [HOTFIX] rm dots when indexing on array
            return self.__RE_RM_ARRAY_DOTS.sub("[", ".".join(reversed(names)))

    def __repr__word(self, index, width, padding, transactionParts):
        buff = ["{0: <{padding}}|".format(index, padding=padding)]
        DW = self.dataWidth

        for tp in reversed(transactionParts):
            percentOfWidth = tp.bit_length() / DW
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
        s = "<%s start:%d, end:%d" % (self.__class__.__name__, self.startBitAddr, self.endBitAddr)
        if not self.parts:
            return s + ">"

        padding = 5
        DW = self.dataWidth
        width = int(DW * scale)

        buff.append('{0: <{padding}}{1: <{halfLineWidth}}{2: >{halfLineWidth}}'.format(
            "", DW - 1, 0, padding=padding, halfLineWidth=width // 2))
        line = '{0: <{padding}}{1:-<{lineWidth}}'.format(
            "", "", padding=padding, lineWidth=width + 1)
        buff.append(line)

        for w, transactionParts in self.walkWords(showPadding=True):
            buff.append(self.__repr__word(w, width, padding, transactionParts))

        buff.append(line)

        return "\n".join(buff)


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
        offset = self.startOfPart % self.parent.dataWidth
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
        return "<TransactionPart startOfPart:%d, endOfPart:%d>" % (
               self.startOfPart, self.endOfPart)
