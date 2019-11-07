from functools import reduce
from math import ceil
from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.typeShortcuts import vec
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.structUtils import walkFlattenFields
from hwt.hdl.value import Value
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class BitWidthErr(Exception):
    """
    Wrong bit width of signal/value
    """


def fitTo_t(what: Union[RtlSignal, Value], where_t: HdlType,
            extend: bool=True, shrink: bool=True):
    """
    Slice signal "what" to fit in "where"
    or
    arithmetically (for signed by MSB / unsigned, vector with 0) extend
    "what" to same width as "where"

    little-endian impl.

    :param extend: allow increasing of the signal width
    :param shrink: allow shrinking of the signal width
    """

    whatWidth = what._dtype.bit_length()
    toWidth = where_t.bit_length()
    if toWidth == whatWidth:
        return what
    elif toWidth < whatWidth:
        # slice
        if not shrink:
            raise BitWidthErr()

        return what[toWidth:]
    else:
        if not extend:
            raise BitWidthErr()

        w = toWidth - whatWidth

        if what._dtype.signed:
            # signed extension
            msb = what[whatWidth - 1]
            ext = reduce(lambda a, b: a._concat(b), [msb for _ in range(w)])
        else:
            # 0 extend
            ext = vec(0, w)

        return ext._concat(what)


def fitTo(what: Union[RtlSignal, Value], where: Union[RtlSignal, Value],
          extend: bool=True, shrink: bool=True):
    return fitTo_t(what, where._dtype, extend, shrink)


class NotEnoughtBitsErr(Exception):
    """
    More bits is required for such an operation
    """


class BitWalker():
    """
    Walker which can walk chunks of bits on signals/values of all types

    :ivar sigOrVal: signal or value to iterate over
    :ivar fillup: flag that means that if there is not enought bits
        for last iterm fill it up with invalid bits (otherwise raise)
    """

    def __init__(self, sigOrVal: Union[RtlSignal, Value],
                 skipPadding: bool=True,
                 fillup: bool=False):
        """
        :param skipPadding: if true padding is skipped in dense types
        """
        self.it = walkFlattenFields(sigOrVal, skipPadding=skipPadding)
        self.fillup = fillup
        self.actuallyHave = 0
        self.actual = None
        self.actualOffset = 0

    @internal
    def _get(self, numberOfBits: int, doCollect: bool):
        """
        :param numberOfBits: number of bits to get from actual possition
        :param doCollect: if False output is not collected just iterator moves
            in structure
        """
        if not isinstance(numberOfBits, int):
            numberOfBits = int(numberOfBits)

        while self.actuallyHave < numberOfBits:
            # accumulate while not has enought
            try:
                f = next(self.it)
            except StopIteration:
                if self.fillup and self.actual is not None:
                    break
                else:
                    raise NotEnoughtBitsErr()

            thisFieldLen = f._dtype.bit_length()
            if self.actual is None:
                if not doCollect and thisFieldLen <= numberOfBits:
                    numberOfBits -= thisFieldLen
                else:
                    self.actual = f
                    self.actuallyHave = thisFieldLen
            else:
                if not doCollect and self.actuallyHave < numberOfBits:
                    self.actuallyHave = thisFieldLen
                    self.actual = f
                else:
                    self.actuallyHave += thisFieldLen
                    self.actual = f._concat(self.actual)

        # slice out from actual
        actual = self.actual
        actualOffset = self.actualOffset

        if self.actuallyHave < numberOfBits:
            assert self.fillup
            if doCollect:
                t = self.actual._dtype
                fillupW = numberOfBits - self.actuallyHave
                padding_t = Bits(fillupW, signed=t.signed, negated=t.negated)
                padding = padding_t.from_py(None)
                actual = padding._concat(actual)
            self.actuallyHave = 0

        # update about what was taken
        self.actuallyHave -= numberOfBits
        self.actualOffset += numberOfBits
        if self.actuallyHave == 0:
            self.actual = None
            self.actualOffset = 0

        if doCollect:
            if numberOfBits == 1:
                return actual[actualOffset]
            else:
                return actual[(actualOffset + numberOfBits):actualOffset]

    def get(self, numberOfBits: int) -> Union[RtlSignal, Value]:
        """
        :param numberOfBits: number of bits to get from actual possition
        :return: chunk of bits of specified size (instance of Value or RtlSignal)
        """
        return self._get(numberOfBits, True)

    def skip(self, numberOfBits: int) -> None:
        """
        Move this iterator without care about item

        :param numberOfBits: number of bits to get from actual possition
        """
        self._get(numberOfBits, False)

    def assertIsOnEnd(self):
        """
        Assert there is nothing left in this iterator
        """
        try:
            next(self.it)
        except StopIteration:
            return

        raise AssertionError("BitWalker there stil were some items")


def iterBits(sigOrVal: Union[RtlSignal, Value], bitsInOne: int=1,
             skipPadding: bool=True, fillup: bool=False):
    """
    Iterate over bits in vector

    :param sigOrVal: signal or value to iterate over
    :param bitsInOne: number of bits in one part
    :param skipPadding: if true padding is skipped in dense types
    """
    bw = BitWalker(sigOrVal, skipPadding, fillup)
    for _ in range(ceil(sigOrVal._dtype.bit_length() / bitsInOne)):
        yield bw.get(bitsInOne)

    bw.assertIsOnEnd()
