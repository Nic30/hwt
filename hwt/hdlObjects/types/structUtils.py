from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.struct import HStructField, HStruct
from hwt.hdlObjects.types.bits import Bits


class FrameTemplateItem(object):
    """
    :ivar name: name of this item, like name in struct field
    :ivar dtype: dtype of this item, like dtype in struct field
    :ivar inFrameBitOffset: number of bits before start of this intem in frame
    :ivar internalInterface: internal interface a
    """
    def __init__(self, name, dtype, inFrameBitOffset, children=None):
        self.name = name
        self.dtype = dtype
        if children is None:
            self.children = []
        else:
            self.children = children

        self.inFrameBitOffset = inFrameBitOffset
        # list of tuples (word index, inWordBitUpper, inWordBitLower)
        self.appearsInWords = []

        self.internalInterface = None


class FrameTemplate(list):

    def walkWords(self):
        """
        Walks frame over words

        :return: generator of tuples (wordIndex, list of FrameTemplateItems)
        """
        wordRecord = []
        actualWord = 0
        if not self[0].appearsInWords:
                raise Exception("resolveFieldPossitionsInFrame has to be called first")
        for fi in self:
            for w, _, _ in fi.appearsInWords:
                if w == actualWord:
                    wordRecord.append(fi)
                elif w > actualWord:
                    yield actualWord, wordRecord
                    wordRecord = [fi, ]
                    actualWord = w
                else:
                    raise NotImplementedError("Input frame info has to be sorted")
    
        if wordRecord:
            yield actualWord, wordRecord
    
    @classmethod
    def _fromHStruct(cls, structT, inFrameOffset, namePrefix):
        for f in structT.fields:
            t = f.dtype
            if isinstance(t, HStruct):
                yield from cls._fromHStruct(t, inFrameOffset, namePrefix + [f.name])
            else:
                fi = FrameTemplateItem(f.name, t, inFrameOffset)
                yield fi

            inFrameOffset += t.bit_length()
        
    
    @classmethod
    def fromHStruct(cls, structT):
        return cls(cls._fromHStruct(structT, 0, []))    
    
    def resolveFieldPossitionsInFrame(self, dataWidth, disolveArrays=True, baseBitAddr=0):
        """
        Format fields in datawords

        :return: number of words
        """
        assert isinstance(dataWidth, int), dataWidth
        bitAddr = baseBitAddr
        for item in self:
            lower = item.inFrameBitOffset % dataWidth
            remInFirstWord = dataWidth - (item.inFrameBitOffset % dataWidth)
            t = item.dtype
            w = t.bit_length()

            if isinstance(t, Array) and not disolveArrays:
                assert lower == 0, "Start of array has to be aligned"
                item.appearsInWords.append((bitAddr // dataWidth, w, 0))
                bitAddr += w
            elif isinstance(t, Array) or isinstance(t, Bits):
                # align start
                if w <= remInFirstWord:
                    upper = lower + w
    
                item.appearsInWords.append((bitAddr // dataWidth, upper, lower))
                if w <= remInFirstWord:
                    bitAddr += w
                    continue
    
                if w // dataWidth > 0:
                    # take aligned middle of field
                    for _ in range(w // dataWidth):
                        item.appearsInWords.append(
                                                   (bitAddr // dataWidth, dataWidth, 0)
                                                  )
                        bitAddr += dataWidth
    
                if w != 0:
                    # take reminder at the end
                    item.appearsInWords.append(
                                               (bitAddr // dataWidth, w, 0)
                                              )
                    bitAddr += w
            elif isinstance(t, HStruct):
                self.resolveFieldPossitionsInFrame(dataWidth, disolveArrays=disolveArrays, baseBitAddr=bitAddr)
                bitAddr += w
            else:
                raise NotImplementedError("Unknown type of field", item.name, t)

        i = bitAddr // dataWidth
        if bitAddr % dataWidth == 0:
            return i
        else:
            return i + 1


class StructFieldPart():
    def __init__(self, wordIndex, busWordBitRange, inFieldBitRange):
        """ranges in little endian notation"""
        self.wordIndex = wordIndex
        self.busWordBitRange = busWordBitRange
        self.inFieldBitRange = inFieldBitRange

    def getSignal(self, busDataSignal):
        if self.busWordBitRange == (busDataSignal._dtype.bit_length(), 0):
            return busDataSignal
        else:
            return busDataSignal[self.busWordBitRange[0]:self.busWordBitRange[1]]

    def __repr__(self):
        return "<StructFieldPart, wordIndex:%d, busWordBitRange:%r, inFieldBitRange:%r>" % (
                self.wordIndex, self.busWordBitRange, self.inFieldBitRange)


class StructFieldInfo():
    def __init__(self, dtype, name):
        self.dtype = dtype
        self.name = name
        self.interface = None
        self.parts = []

    def discoverFieldParts(self, busDataWidth, startBitIndex):
        """Some fields has to be internally split due data-width of bus,
        there we discover how to split field to words on bus

        :param startWordIndex: bit index where field starts, (f.e. 16 for f2 in struct {uint16_t f1, uint16_t f2})

        """
        fieldWidth = self.dtype.bit_length()
        inFieldOffset = 0

        while fieldWidth != 0:
            wordIndex = startBitIndex // busDataWidth
            bitRangeOfWord = (busDataWidth * (wordIndex + 1), startBitIndex)  # little-endian
            widthOfPart = min(bitRangeOfWord[0], startBitIndex + fieldWidth) - startBitIndex
            busWordBitOffset = startBitIndex % busDataWidth

            busWordBitRange = (busWordBitOffset + widthOfPart, busWordBitOffset)
            inFieldRange = (inFieldOffset + widthOfPart, inFieldOffset)

            fp = StructFieldPart(wordIndex, busWordBitRange, inFieldRange)
            self.parts.append(fp)

            inFieldOffset += widthOfPart
            startBitIndex += widthOfPart
            fieldWidth -= widthOfPart

        return startBitIndex + fieldWidth

    def __repr__(self):
        return "<StructFieldInfo %s, %r, parts:%s  >" % (
            self.name, self.dtype, "\n".join(["%r" % s for s in self.parts]))


class StructBusBurstInfo():
    """
    Represents data chunks(bursts) which should be send over interface
    container of parts of fields form struct
    """
    def __init__(self, addrOffset, fieldInfos):
        """
        :param addrOffset: offset of this burst in number of words
        :param fieldInfos: iterable of field StructFieldInfo
        """
        self.addrOffset = addrOffset
        self.fieldInfos = fieldInfos

    def wordCnt(self):
        firstWordIndex = self.fieldInfos[0].parts[0].wordIndex
        lastWordIndex = self.fieldInfos[-1].parts[-1].wordIndex

        return lastWordIndex - firstWordIndex + 1

    @staticmethod
    def packFieldInfosToBusBurst(structInfos, maxDummyWords, wordIndexToAddrRatio):
        """
        :param structInfos: iterable of StructFieldInfo which are describing target structure
        :param maxDummyWords: maximum allowable not used words in bus burst
        :param wordIndexToAddrRatio: addrOffset = wordIndex of field * wordIndexToAddrRatio
        :return: list of StructBusBurstInfo
        """
        busBursts = []

        try:
            firstWordIndex = structInfos[0].parts[0].wordIndex
        except IndexError:
            return []

        lastWordIndex = firstWordIndex
        actual = StructBusBurstInfo(lastWordIndex * wordIndexToAddrRatio, [])
        skippedWords = 0
        busBursts.append(actual)

        # for each part which should be download
        for info in structInfos:
            # check if space between fields is small enough
            startW = info.parts[0].wordIndex
            if startW - lastWordIndex - skippedWords > maxDummyWords:
                # space between useful fields is too big and we have to split burst into multiple smaller
                skippedWords += startW - lastWordIndex - 2
                actual = StructBusBurstInfo(startW * wordIndexToAddrRatio, [])
                busBursts.append(actual)

            if skippedWords != 0:
                # update word indexes after unused fields were potentially cut of
                for p in info.parts:
                    p.wordIndex -= skippedWords

            actual.fieldInfos.append(info)
            lastWordIndex = info.parts[-1].wordIndex

        return busBursts

    @staticmethod
    def sumOfWords(structBusBurstInfos):
        return structBusBurstInfos[-1].fieldInfos[-1].parts[-1].wordIndex + 1

    def __repr__(self):
        return "<StructBusBurstInfo addrOffset:%d>" % self.addrOffset



class BusFieldInfo(object):
    def __init__(self, access="rw", fieldInterface=None, disolveArray=False):
        """
        :param access: "r", "w" or "rw" describes access mode from bus side
        :param fieldInterface: interface for which this field was generated
        :param disolveArray: interpret this array interface as bunch of items
                             instead of single memory space
        """
        assert access in ['r', 'w', 'rw']
        self.access = access
        self.fieldInterface = fieldInterface
        self.disolveArray = disolveArray

def HStruct_selectFields(structT, fieldsToUse):
    """
    Select fields from structure (rest will become spacing)
    
    :param structT: HStruct type instance
    :param fieldsToUse: dict {name:{...}} or set of names to select, dictionary is used to select nested fields
        in HStruct or HUnion fields (f.e. {"struct1": {"field1", "field2"}, "field3":{}} 
        will select field1 and 2 from struct1 and field3 from root)
    """

    template = []
    fieldsToUse = fieldsToUse
    foundNames = set()

    for f in structT.fields:
        name = None
        subfields = []

        if f.name is not None:
            try:
                if isinstance(fieldsToUse, dict):
                    subfields = fieldsToUse[f.name]
                    name = f.name
                else:
                    if f.name in fieldsToUse:
                        name = f.name
            except KeyError:
                name = None
        
        if name is not None and subfields:
            template.append(HStructField(HStruct_selectFields(f.dtype, subfields), name))
        else:
            template.append(HStructField(f.dtype, name))
        
        if f.name is not None:
            foundNames.add(f.name)

    if isinstance(fieldsToUse, dict):
        fieldsToUse = set(fieldsToUse.keys())
    assert fieldsToUse.issubset(foundNames)

    return HStruct(*template)

