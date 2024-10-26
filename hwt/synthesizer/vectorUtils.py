from math import ceil
from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.utils import walkFlattenFields
from hwt.mainBases import RtlSignalBase


class NotEnoughtBitsErr(Exception):
    """
    More bits is required for such an operation
    """


class BitWalker():
    """
    Walker which can walk chunks of bits on signals/values of all types

    :ivar ~.sigOrConst: signal or value to iterate over
    :ivar ~.fillup: flag that means that if there is not enough bits
        for last item fill it up with invalid bits (otherwise raise)
    """

    def __init__(self, sigOrConst: Union[RtlSignalBase, HConst],
                 skipPadding: bool=True,
                 fillup: bool=False):
        """
        :param skipPadding: if true padding is skipped in dense types
        """
        self.it = walkFlattenFields(sigOrConst, skipPadding=skipPadding)
        self.fillup = fillup
        self.actuallyHave = 0
        self.actual = None
        self.actualOffset = 0

    @internal
    def _get(self, numberOfBits: int, doCollect: bool):
        """
        :param numberOfBits: number of bits to get from actual position
        :param doCollect: if False output is not collected just iterator moves
            in data structure
        """
        if not isinstance(numberOfBits, int):
            numberOfBits = int(numberOfBits)

        while self.actuallyHave < numberOfBits:
            # accumulate while not has enough
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
                padding_t = HBits(fillupW, signed=t.signed, negated=t.negated)
                padding = padding_t.from_py(None)
                actual = padding._concat(actual)
            self.actuallyHave = 0
            self.actualOffset = 0
        else:
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

    def get(self, numberOfBits: int) -> Union[RtlSignalBase, HConst]:
        """
        :param numberOfBits: number of bits to get from actual position
        :return: chunk of bits of specified size (instance of Value or RtlSignal)
        """
        return self._get(numberOfBits, True)

    def skip(self, numberOfBits: int) -> None:
        """
        Move this iterator without care about item

        :param numberOfBits: number of bits to get from actual position
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

        raise AssertionError("there are still some items")


def iterBits(sigOrConst: Union[RtlSignalBase, HConst], bitsInOne: int=1,
             skipPadding: bool=True, fillup: bool=False):
    """
    Iterate over bits in vector

    :param sigOrConst: signal or value to iterate over
    :param bitsInOne: number of bits in one part
    :param skipPadding: if true padding is skipped in dense types
    :param fillup: flag that means that if there is not enough bits
        for last item fill it up with invalid bits (otherwise raise)
    """
    bw = BitWalker(sigOrConst, skipPadding, fillup)
    try:
        bit_len = sigOrConst._dtype.bit_length()
    except TypeError:
        bit_len = None
    if bit_len is None:
        try:
            while True:
                yield bw.get(bitsInOne)
        except NotEnoughtBitsErr:
            return
    else:
        for _ in range(ceil(bit_len / bitsInOne)):
            yield bw.get(bitsInOne)

        bw.assertIsOnEnd()
