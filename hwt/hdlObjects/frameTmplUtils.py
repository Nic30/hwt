from hwt.hdlObjects.transTmpl import OneOfTransaction
from hwt.hdlObjects.transactionPart import TransactionPart


def iterSort(iterators, cmpFn):
    """
    Sort items from iterators(generators) by alwas selecting item with lowest value
    (min first)

    :return: generator of tuples (origin index, item) where origin index is index
        of iterator in "iterators" from where item commes from
    """
    actual = []
    _iterators = []
    for i, it in enumerate(iterators):
        try:
            a = next(it)
            _iterators.append((i, it))
            actual.append(a)
        except StopIteration:
            continue

    while True:
        if not _iterators:
            return
        elif len(_iterators) == 1:
            originIndex, it = _iterators[0]
            yield originIndex, actual[0]
            for item in it:
                yield originIndex, item
            return

        # select minimum and iterator from where it comes from
        minimum = None
        minimumIndex = None
        secondMin = None
        for i, val in enumerate(actual):
            skipSecMinCheck = False
            if minimum is None:
                minimum = val
                minimumIndex = i
            elif cmpFn(val, minimum):
                secondMin = minimum
                minimum = val
                minimumIndex = i
                skipSecMinCheck = True
            elif not skipSecMinCheck and (
                    secondMin is None or cmpFn(val, secondMin)):
                secondMin = val

        actualI, actualIt = _iterators[minimumIndex]
        while not cmpFn(secondMin, minimum):
            yield (actualI, minimum)
            try:
                minimum = next(actualIt)
            except StopIteration:
                minimum = None
                break

        # consume from actual iterator while
        if minimum is None:
            del _iterators[minimumIndex]
            del actual[minimumIndex]
        else:
            # minimum is not minimum anymore
            actual[minimumIndex] = minimum


class ChoiceOfFrameParts(list):
    """
    List of lists of transaction parts
    One of child list is used to represent the word, item depends
    on context

    :ivar startOfPart: bit addr of start of this group of frame parts
    :ivar origin: OneOfTransaction instance
    """
    def __init__(self, startOfPart, origin):
        self.origin = origin
        self.startOfPart = startOfPart
        self.endOfPart = None

    def resolveEnd(self):
        end = self.startOfPart
        for items in self:
            if items:
                end = max(end, max(itm.endOfPart for itm in items))
        self.endOfPart = end

    def bit_length(self):
        return self.endOfPart - self.startOfPart

    def __repr__(self):
        return "<ChoiceOfFrameParts %s>" % list.__repr__(self)


def groupIntoChoices(splitsOnWord, wordWidth, origin):
    """
    :param: splitsOnWord list of lists of parts (fields splited on word
        boundaries)
    :return: generators of ChoiceOfFrameParts for each word
        which are not crossing word boundaries
    """
    def cmpWordIndex(a, b):
        return a.startOfPart // wordWidth < b.startOfPart // wordWidth

    actual = None
    itCnt = len(splitsOnWord)
    for i, item in iterSort(splitsOnWord, cmpWordIndex):
        _actualW = item.startOfPart // wordWidth
        if actual is None:
            actual = ChoiceOfFrameParts(item.startOfPart, origin)
            actual.extend([] for _ in range(itCnt))
            actualW = _actualW
        elif _actualW > actualW:
            actual.resolveEnd()
            yield actual
            actual = ChoiceOfFrameParts(item.startOfPart, origin)
            actual.extend([] for _ in range(itCnt))
            actualW = _actualW
        actual[i].append(item)

    if actual is not None:
            actual.resolveEnd()
            yield actual


class TransTmplWordIterator():
    def __init__(self, wordWidth):
        self.wordWidth = wordWidth

    def fullWordCnt(self, start, end):
        """Count of complete words between two addresses
        """
        assert end >= start, (start, end)
        gap = max(0, (end - start) - (start % self.wordWidth))
        return gap // self.wordWidth

    def groupByWordIndex(self, transaction, offset):
        """
        Group transaction parts splited on words to words

        :return: generator of tuples (wordIndex, list of transaction parts in this word)
        """
        actualW = None
        partsInWord = []
        wordWidth = self.wordWidth
        for item in self.splitOnWords(transaction, offset):
            _actualW = item.startOfPart // wordWidth
            if actualW is None:
                actualW = _actualW
                partsInWord.append(item)
            elif _actualW > actualW:
                yield (actualW, partsInWord)
                actualW = _actualW
                partsInWord = [item, ]
            else:
                partsInWord.append(item)

        if partsInWord:
            yield (actualW, partsInWord)

    def splitOnWords(self, transaction, addrOffset=0):
        """
        :return: generator of TransactionPart instance
        """
        wordWidth = self.wordWidth
        end = addrOffset
        for tmp in transaction.walkFlatten(offset=addrOffset):
            if isinstance(tmp, OneOfTransaction):
                split = [self.splitOnWords(ch, end)
                         for ch in tmp.possibleTransactions]
                yield from groupIntoChoices(split, wordWidth, tmp)
                end = addrOffset + tmp.possibleTransactions[0].bitAddrEnd
            else:
                (base, end), tmpl = tmp
                startOfPart = base
                while startOfPart != end:
                    wordIndex = startOfPart // wordWidth
                    endOfWord = (wordIndex + 1) * wordWidth
                    endOfPart = min(endOfWord, end)
                    inFieldOffset = startOfPart - base
                    yield TransactionPart(tmpl, startOfPart, endOfPart, inFieldOffset)
                    startOfPart = endOfPart
