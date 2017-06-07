from math import ceil, floor, inf
import re

from hwt.hdlObjects.transactionPart import TransactionPart
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.struct import HStruct
from hwt.simulator.types.simBits import simBitsT
from hwt.bitmask import mask, selectBitRange, setBitRange


def walkFlatten(transactionTmpl, offset=None, shouldEnterFn=lambda transTmpl: True):
    """
    Walk fields in instance of TransTmpl
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
    """
    Frame template container for informations about frame,
    template which is used for resolving how data should be formated into words and frames
    on target interface

    :ivar _fieldToTPart:
    """
    __RE_RM_ARRAY_DOTS = re.compile("(\.\[)")

    def __init__(self, origin, wordWidth, startBitAddr, endBitAddr, transactionParts):
        """
        :param origin: instance of HType (usually HStruct) from which this FrameTemplate was generated from
        :param wordWidth: width of word on interface where this template should be used
        :param startBitAddr: bit offset where this frame starts
        :param endBitAddr: bit offset where this frame ends (bit index of first bit behind this frame)
        :param transactionParts: instances of TransactionPart which are parts of this frame
        """
        self.origin = origin
        self.wordWidth = wordWidth
        self.startBitAddr = startBitAddr
        self.endBitAddr = endBitAddr
        self.parts = transactionParts

        self._fieldToTPart = None
        
        for p in self.parts:
            p.parent = self
            assert p.startOfPart >= startBitAddr, (p, startBitAddr, self)
            assert p.endOfPart <= endBitAddr, (p, endBitAddr, self)

    @staticmethod
    def frameFromTransTmpl(transactionTmpl,
                           wordWidth,
                           maxPaddingWords=inf,
                           trimPaddingWordsOnStart=False,
                           trimPaddingWordsOnEnd=False):
        """
        Params same as framesFromTransTmpl
        """
        return next(FrameTemplate.framesFromTransTmpl(transactionTmpl,
                                                      wordWidth,
                                                      maxPaddingWords=maxPaddingWords,
                                                      trimPaddingWordsOnStart=trimPaddingWordsOnStart,
                                                      trimPaddingWordsOnEnd=trimPaddingWordsOnEnd))
    
    @staticmethod
    def framesFromTransTmpl(transactionTmpl,
                            wordWidth,
                            maxFrameLen=inf,
                            maxPaddingWords=inf,
                            trimPaddingWordsOnStart=False,
                            trimPaddingWordsOnEnd=False):
        """
        Convert transaction template into FrameTemplates

        :param transactionTmpl: transaction template used which are FrameTemplates created from
        :param wordWidth: width of data signal in target interface where frames will be used
        :param maxFrameLen: maximum length of frame, if exceeded another frame will be created
        :param maxPaddingWords: maximum of continual padding words in frame,
            if exceed frame is split and words are cut of
        :attention: if maxPaddingWords<inf trimPaddingWordsOnEnd or trimPaddingWordsOnStart has to be True
            to decide where padding should be trimmed
        :param trimPaddingWordsOnStart: trim padding from start of frame at word granularity
        :param trimPaddingWordsOnEnd: trim padding from end of frame at word granularity
        """
        isFirstInFrame = True
        partsPending = False

        startOfThisFrame = 0
        endOfThisFrame = maxFrameLen
        parts = []
        endOfPart = 0
        assert maxFrameLen > 0
        assert maxPaddingWords >= 0
        if maxPaddingWords < inf:
            assert trimPaddingWordsOnStart or trimPaddingWordsOnEnd

        def fullWordCnt(start, end):
            """Count of complete words between two addresses
            """
            startWIndex = start // wordWidth
            endWIndex = end // wordWidth

            assert startWIndex <= endWIndex, (start, end)

            return endWIndex - startWIndex

        for (base, end), tmpl in walkFlatten(transactionTmpl):
            startOfPart = base
            while startOfPart != end:
                assert startOfThisFrame % wordWidth == 0, startOfThisFrame
                # parts are always in single word
                if startOfPart == endOfThisFrame:
                    # cut off padding at end of frame
                    paddingWords = fullWordCnt(endOfPart, endOfThisFrame)
                    if trimPaddingWordsOnEnd and paddingWords > maxPaddingWords:
                        _endOfThisFrame = endOfThisFrame - paddingWords * wordWidth
                        # align end of frame to word
                        _endOfThisFrame = ceil(_endOfThisFrame / wordWidth) * wordWidth

                    yield FrameTemplate(wordWidth, startOfThisFrame, _endOfThisFrame, parts)

                    # prepare for start of new frame
                    parts = []
                    isFirstInFrame = True
                    partsPending = False
                    # start on new
                    startOfThisFrame = (endOfThisFrame // wordWidth) * wordWidth
                    endOfThisFrame = startOfThisFrame + maxFrameLen
                    endOfPart = endOfThisFrame

                    continue

                if isFirstInFrame:
                    partsPending = True
                    isFirstInFrame = False
                    # cut off padding at start of frame
                    paddingWords = fullWordCnt(startOfThisFrame, base)
                    if trimPaddingWordsOnStart and paddingWords > maxPaddingWords:
                        startOfThisFrame += paddingWords * wordWidth

                    endOfThisFrame = startOfThisFrame + maxFrameLen
                else:
                    padding = startOfPart - endOfPart
                    if trimPaddingWordsOnEnd and padding >= wordWidth:
                        # there is too much continual padding
                        endOfThisFrame = startOfPart
                        continue

                wordIndex = startOfPart // wordWidth
                endOfWord = wordWidth * (wordIndex + 1)

                endOfPart = min(endOfWord, end, endOfThisFrame)

                inFieldOffset = end - endOfPart
                p = TransactionPart(tmpl, startOfPart, endOfPart, inFieldOffset)
                parts.append(p)

                startOfPart = endOfPart

        if partsPending:
            endOfThisFrame = max(startOfPart, transactionTmpl.bitAddrEnd)
            # cut off padding at end of frame
            paddingWords = fullWordCnt(endOfPart, endOfThisFrame)
            if trimPaddingWordsOnEnd and paddingWords > maxPaddingWords:
                endOfThisFrame -= paddingWords * wordWidth
                # align end of frame to word
            endOfThisFrame = ceil(endOfThisFrame / wordWidth) * wordWidth

            yield FrameTemplate(wordWidth, startOfThisFrame, endOfThisFrame, parts)

    def _wordIndx(self, addr):
        """
        convert bit address to index of word where this address is
        """
        return floor(addr / self.wordWidth)

    def getWordCnt(self):
        """
        Get count of words in this frame
        """
        return ceil((self.endBitAddr - self.startBitAddr) / self.wordWidth)

    def walkWords(self, showPadding=False):
        """
        Walk enumerated words in this frame

        :attention: not all indexes has to be present, only words with items will be generated when not showPadding
        :param showPadding: padding TransactionParts are also present
        :return: generator of tuples (wordIndex, list of TransactionParts in this word)
        """
        wIndex = 0
        lastEnd = self.startBitAddr
        parts = []
        for p in self.parts:
            end = p.startOfPart
            if showPadding and end != lastEnd:
                # insert padding
                while end != lastEnd:
                    assert end >= lastEnd, (end, lastEnd)
                    endOfWord = (self._wordIndx(lastEnd) + 1) * self.wordWidth
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
            if lastEnd % self.wordWidth == 0:
                yield (wIndex, parts)

                wIndex += 1
                parts = []

        if showPadding and (parts or lastEnd != self.endBitAddr or lastEnd % self.wordWidth != 0):
            end = (self._wordIndx(self.endBitAddr - 1) + 1) * self.wordWidth
            if showPadding:
                while end != lastEnd:
                    assert end >= lastEnd, (end, lastEnd)
                    endOfWord = lastEnd + self.wordWidth
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

    @staticmethod
    def buildFieldToDataDict(dtype, data, res):
        # assert data is None or isinstance(data, dict)
        for f in dtype.fields:
            try:
                fVal = data[f.name]
            except KeyError:
                fVal = None
            
            if isinstance(f.dtype, Bits):
                if fVal is not None:
                    assert isinstance(fVal, int)
                    res[f] = fVal
            elif isinstance(f.dtype, HStruct):
                if fVal:
                    FrameTemplate.buildFieldToDataDict(f.dtype, fVal, res)
            elif isinstance(f.dtype, Array):
                if fVal:
                    # assert isinstance(fVal, class_or_tuple)
                    res[f] = fVal
        
        return res
    
    def packData(self, data):
        """
        Pack data into list of BitsVal of specified dataWidth
    
        :param data: dict of values for struct fields {fieldName: value}
    
        :return: list of BitsVal which are representing values of words
        """
        typeOfWord = simBitsT(self.wordWidth, None)
        fieldToVal = self._fieldToTPart
        if fieldToVal is None:
            fieldToVal = self._fieldToTPart = self.buildFieldToDataDict(self.origin, data)

        for _, transactionParts in self.walkWords(showPadding=True):
            actualVldMask = 0
            actualVal = 0
            for tPart in transactionParts:
                high, low = tPart.getBusWordBitRange()
                fhigh, flow = tPart.getFieldBitRange()
                if not tPart.isPadding:
                    val = fieldToVal.get(tPart.tmpl.origin, None)
                else:
                    val = None
    
                if val is None:
                    newBits = 0
                    vld = 0
                else:
                    newBits = selectBitRange(val, flow, fhigh - flow)
                    vld = mask(high - low) << low
    
                setBitRange(actualVal, low, high - low, newBits)
                setBitRange(actualVal, low, high - low, vld)
                    
            yield typeOfWord.getValueCls()(actualVal, typeOfWord, actualVldMask, -1)

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
        DW = self.wordWidth

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
        DW = self.wordWidth
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
