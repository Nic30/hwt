from itertools import zip_longest
from math import ceil, floor, inf
from typing import Union, Generator, List

from hwt.doc_markers import internal
from hwt.hdl.frameTmplUtils import TransTmplWordIterator, \
    ChoicesOfFrameParts
from hwt.hdl.transPart import TransPart
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStruct
from hwt.pyUtils.arrayQuery import flatten
from pyMathBitPrecise.bit_utils import mask, get_bit_range, set_bit_range


class FrameTmpl(object):
    """
    Frame template is metainfomation about data structure, it's the template
    of transaction for specific interface

    Usuall flow of frame generatig consists of these steps:

    1. Describe format of data by HDL type (HStruct, HUnion ...)

    2. Convert it to TransTmpl to resolve addresses of each field in structure

    3. Split parts of TransTmpl into words

    4. Use parts in words to assembly frames

    :ivar ~._fieldToTPart: dictionary {HStructField: TransPart} to resolve
        this association, None by default, builded when packData
        is called and is not builded
    :note: others ivars described in __init__
    """

    def __init__(self, origin: HdlType,
                 wordWidth: int,
                 startBitAddr: int,
                 endBitAddr: int,
                 transParts: List[TransPart]):
        """
        :param origin: instance of HType (usually HStruct)
            from which this FrameTmpl was generated from
        :param wordWidth: width of word on interface
            where this template should be used
        :param startBitAddr: bit offset where this frame starts
        :param endBitAddr: bit offset where this frame ends
            (bit index of first bit behind this frame)
        :param transParts: instances of TransPart which are parts of this frame
        """
        self.origin = origin
        self.wordWidth = wordWidth
        assert startBitAddr <= endBitAddr
        self.startBitAddr = startBitAddr
        self.endBitAddr = endBitAddr
        self.parts = transParts

        self._fieldToTPart = None

        for p in self.parts:
            p.parent = self
            assert p.startOfPart >= startBitAddr, (p, startBitAddr)
            assert p.endOfPart <= endBitAddr, (p, endBitAddr)

    @staticmethod
    def framesFromTransTmpl(transaction: 'TransTmpl',
                            wordWidth: int,
                            maxFrameLen: Union[int, float]=inf,
                            maxPaddingWords: Union[int, float]=inf,
                            trimPaddingWordsOnStart: bool=False,
                            trimPaddingWordsOnEnd: bool=False) -> Generator[
                                'FrameTmpl', None, None]:
        """
        Convert transaction template into FrameTmpls

        :param transaction: transaction template used which are FrameTmpls
            created from
        :param wordWidth: width of data signal in target interface
            where frames will be used
        :param maxFrameLen: maximum length of frame in bits,
            if exceeded another frame will be created
        :param maxPaddingWords: maximum of continual padding words in frame,
            if exceed frame is split and words are cut of
        :attention: if maxPaddingWords<inf trimPaddingWordsOnEnd
            or trimPaddingWordsOnStart has to be True
            to decide where padding should be trimmed
        :param trimPaddingWordsOnStart: trim padding from start of frame
            at word granularity
        :param trimPaddingWordsOnEnd: trim padding from end of frame
            at word granularity
        """
        isFirstInFrame = True
        partsPending = False

        startOfThisFrame = 0
        assert maxFrameLen > 0
        assert maxPaddingWords >= 0
        if maxPaddingWords < inf:
            assert trimPaddingWordsOnStart or trimPaddingWordsOnEnd, \
                "Padding has to be cut off somewhere"

        it = TransTmplWordIterator(wordWidth)
        lastWordI = 0
        endOfThisFrame = maxFrameLen
        parts = []
        for wordI, word in it.groupByWordIndex(transaction, 0):
            if wordI * wordWidth >= endOfThisFrame:
                # now in first+ word behind the frame
                # cut off padding at end of frame
                paddingWords = wordI - lastWordI
                if trimPaddingWordsOnEnd and paddingWords > maxPaddingWords:
                    # cut off padding and align end of frame to word
                    _endOfThisFrame = (lastWordI + 1) * wordWidth
                else:
                    _endOfThisFrame = wordI * wordWidth

                yield FrameTmpl(transaction,
                                wordWidth,
                                startOfThisFrame,
                                _endOfThisFrame,
                                parts)

                # prepare for start of new frame
                parts = []
                isFirstInFrame = True
                partsPending = False
                # start on new word
                startOfThisFrame = _endOfThisFrame
                endOfThisFrame = startOfThisFrame + maxFrameLen
                lastWordI = wordI

            # check if padding at potential end of frame can be cut off
            if (not isFirstInFrame
                    and trimPaddingWordsOnEnd
                    and wordI - lastWordI > 1):
                # there is too much continual padding,
                # cut it out and start new frame
                _endOfThisFrame = (lastWordI + 1) * wordWidth
                yield FrameTmpl(transaction,
                                wordWidth,
                                startOfThisFrame,
                                _endOfThisFrame,
                                parts)

                # prepare for start of new frame
                parts = []
                isFirstInFrame = True
                partsPending = False
                # start on new word
                lastWordI = wordI - 1
                startOfThisFrame = lastWordI * wordWidth
                endOfThisFrame = startOfThisFrame + maxFrameLen

            if isFirstInFrame:
                partsPending = True
                isFirstInFrame = False
                # cut off padding at start of frame
                paddingWords = wordI - lastWordI
                if trimPaddingWordsOnStart and paddingWords > maxPaddingWords:
                    startOfThisFrame += paddingWords * wordWidth

                endOfThisFrame = startOfThisFrame + maxFrameLen

            # resolve end of this part
            parts.extend(word)
            lastWordI = wordI

        # reminder in "parts" after last iteration
        endOfThisFrame = transaction.bitAddrEnd
        withPadding = not (trimPaddingWordsOnEnd or trimPaddingWordsOnStart)
        if partsPending or (withPadding
                            and endOfThisFrame != startOfThisFrame):
            # cut off padding at end of frame
            endOfLastWord = (lastWordI + 1) * wordWidth
            if endOfThisFrame < endOfLastWord:
                endOfThisFrame = endOfLastWord
            else:
                paddingWords = it.fullWordCnt(endOfLastWord, endOfThisFrame)
                if trimPaddingWordsOnEnd and paddingWords > maxPaddingWords:
                    endOfThisFrame -= paddingWords * wordWidth
                    # align end of frame to word
            endOfThisFrame = min(startOfThisFrame + 
                                 maxFrameLen, endOfThisFrame)

            yield FrameTmpl(transaction,
                            wordWidth,
                            startOfThisFrame,
                            endOfThisFrame,
                            parts)
            parts = []
            startOfThisFrame = endOfThisFrame

        # final padding on the end
        while withPadding and startOfThisFrame < transaction.bitAddrEnd:
            endOfThisFrame = min(startOfThisFrame + 
                                 maxFrameLen, transaction.bitAddrEnd)

            yield FrameTmpl(transaction,
                            wordWidth,
                            startOfThisFrame,
                            endOfThisFrame,
                            [])

            startOfThisFrame = endOfThisFrame

    @internal
    def _wordIndx(self, addr: int):
        """
        convert bit address to index of word where this address is
        """
        return floor(addr / self.wordWidth)

    def getWordCnt(self):
        """
        Get count of words in this frame
        """
        return ceil((self.endBitAddr - self.startBitAddr) / self.wordWidth)

    def walkWords(self, showPadding: bool=False):
        """
        Walk enumerated words in this frame

        :attention: not all indexes has to be present, only words
            with items will be generated when not showPadding
        :param showPadding: padding TransParts are also present
        :return: generator of tuples (wordIndex, list of TransParts
            in this word)
        """
        wIndex = 0
        lastEnd = self.startBitAddr
        parts = []
        for p in self.parts:
            end = p.startOfPart
            if showPadding and end != lastEnd:
                # insert padding before data
                while end != lastEnd:
                    assert end >= lastEnd, (end, lastEnd)
                    endOfWord = ceil(
                        (lastEnd + 1) / self.wordWidth) * self.wordWidth
                    endOfPadding = min(endOfWord, end)
                    _p = TransPart(self, None, False, lastEnd, endOfPadding, 0)
                    parts.append(_p)

                    if endOfPadding >= endOfWord:
                        yield (wIndex, parts)
                        wIndex += 1
                        parts = []

                    lastEnd = endOfPadding

            if self._wordIndx(lastEnd) != self._wordIndx(p.startOfPart):
                # if input data continues to a next word, yield current word
                # and start processing next one
                yield (wIndex, parts)

                wIndex += 1
                parts = []
                lastEnd = p.endOfPart

            parts.append(p)
            lastEnd = p.endOfPart
            if lastEnd % self.wordWidth == 0:
                # if we can not add anything to this word,
                # yield it directly and continue on next word
                yield (wIndex, parts)

                wIndex += 1
                parts = []

        if showPadding and (parts
                            or lastEnd != self.endBitAddr
                            or lastEnd % self.wordWidth != 0):
            # align end to end of last word
            end = ceil(self.endBitAddr / self.wordWidth) * self.wordWidth
            # padding is non removable if it is part of data
            # and it is removable if it was generated by frame alignment
            endOfNonRemovablePadding = self.origin.bitAddrEnd
            while end != lastEnd:
                assert end >= lastEnd, (end, lastEnd)
                endOfWord = ((lastEnd // self.wordWidth) + 1) * self.wordWidth
                endOfPadding = min(endOfWord, end)
                if lastEnd < endOfNonRemovablePadding:
                    endOfPadding = min(endOfPadding, endOfNonRemovablePadding)
                    can_be_removed = False
                else:
                    can_be_removed = True
                _p = TransPart(self, None, can_be_removed,
                               lastEnd, endOfPadding, 0)
                _p.parent = self
                parts.append(_p)

                if endOfPadding >= endOfWord:
                    yield (wIndex, parts)
                    wIndex += 1
                    parts = []

                lastEnd = endOfPadding

        if parts:
            # in the case end of frame is not aligned to end of word
            yield (wIndex, parts)

    @staticmethod
    def fieldToDataDict(dtype, data, res):
        return FrameTmpl._fieldToDataDict(dtype, (dtype,), data, res)

    @staticmethod
    def _fieldToDataDict(dtype, path, data, res):
        """
        Construct dictionary {StructField:value} for faster lookup of values
        for fields
        """
        # assert data is None or isinstance(data, dict)
        for f in dtype.fields:
            try:
                fVal = data[f.name]
            except KeyError:
                fVal = None

            new_path = (*path, f)
            if isinstance(f.dtype, Bits):
                if fVal is not None:
                    assert isinstance(fVal, int)
                    res[new_path] = fVal
            elif isinstance(f.dtype, HStruct):
                if fVal:
                    FrameTmpl._fieldToDataDict(f.dtype, new_path, fVal, res)
            elif isinstance(f.dtype, HArray):
                if fVal:
                    # assert isinstance(fVal, class_or_tuple)
                    res[new_path] = fVal

        return res

    def packData(self, data):
        """
        Pack data into list of BitsVal of specified dataWidth

        :param data: dict of values for struct fields {fieldName: value}

        :return: list of BitsVal which are representing values of words
        """
        typeOfWord = Bits(self.wordWidth, None)
        fieldToVal = self._fieldToTPart
        if fieldToVal is None:
            fieldToVal = self._fieldToTPart = self.fieldToDataDict(
                self.origin.dtype,
                data,
                {})

        for _, transParts in self.walkWords(showPadding=True):
            # build a single data word
            actualVldMask = 0
            actualVal = 0
            for tPart in transParts:
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
                    newBits = get_bit_range(val, flow, fhigh - flow)
                    vld = mask(high - low)

                actualVal = set_bit_range(actualVal, low, high - low, newBits)
                actualVldMask = set_bit_range(actualVldMask, low, high - low, vld)

            v = typeOfWord.getValueCls()(typeOfWord, actualVal,
                                         actualVldMask)
            yield v

    @internal
    def __repr__getName(self, transPart: TransPart, fieldWidth: int):
        """
        Get name string for a field
        """
        if transPart.isPadding:
            return "X" * fieldWidth
        else:
            path = transPart.tmpl.getFieldPath()
            names = []
            for p in path:
                if isinstance(p, int):
                    names.append("[%d]" % p)
                else:
                    if names:
                        names.append(".%s" % p)
                    else:
                        names.append(p)

            return "".join(names)

    @internal
    def __repr__word(self,
                     index: int,
                     width: int,
                     padding: int,
                     transParts: List[TransPart]):
        buff = ["{0: <{padding}}|".format(index, padding=padding)]
        DW = self.wordWidth
        partsWithChoice = []

        endAlignment = transParts[-1].endOfPart % DW
        if endAlignment:
            # -1 for ending |
            percentOfWidth = (DW - endAlignment) / DW
            # -1 for ending |
            fieldWidth = max(0, int(percentOfWidth * width) - 1)
            assert fieldWidth >= 0
            s = '%s|' % ("^" * fieldWidth)
            buff.append(s)

        for tp in reversed(transParts):
            percentOfWidth = tp.bit_length() / DW
            # -1 for ending |
            fieldWidth = max(0, int(percentOfWidth * width) - 1)
            assert fieldWidth >= 0

            # percentOffset = (tp.inFrameBitAddr % DW) / DW
            # offset = int(percentOffset * width)
            if isinstance(tp, ChoicesOfFrameParts):
                name = "<union>"
                partsWithChoice.append(tp)
            else:
                name = self.__repr__getName(tp, fieldWidth)
            buff.append('{0: ^{fieldWidth}}|'.format(
                name, fieldWidth=fieldWidth))
        return ("".join(buff), partsWithChoice)

    def __repr__(self, scale=1):
        buff = []
        s = "<%s start:%d, end:%d" % (
            self.__class__.__name__, self.startBitAddr, self.endBitAddr)
        buff.append(s)

        padding = 5
        DW = self.wordWidth
        width = int(DW * scale)

        buff.append(
            '{0: <{padding}}{1: <{halfLineWidth}}{2: >{halfLineWidth}}'.format(
                "", DW - 1, 0, padding=padding, halfLineWidth=width // 2))
        line = '{0: <{padding}}{1:-<{lineWidth}}'.format(
            "", "", padding=padding, lineWidth=width + 1)
        buff.append(line)

        for w, transParts in self.walkWords(showPadding=True):
            wStr, partsWithChoice = self.__repr__word(
                w, width, padding, transParts)
            buff.append(wStr)
            while partsWithChoice:
                for parts in zip_longest(*partsWithChoice):
                    parts = list(flatten(parts, level=1))
                    wStr, _partsWithChoice = self.__repr__word(
                        w, width, padding, parts)
                    buff.append(wStr)
                partsWithChoice = _partsWithChoice

        buff.append(line)
        buff.append(">")
        return "\n".join(buff)
