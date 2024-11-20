from typing import Union

from hwt.constants import DIRECTION
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsConst import HBitsConst
from hwt.mainBases import HwIOBase
from hwt.mainBases import RtlSignalBase


class NotSpecifiedError(Exception):
    """
    This error means that you need to implement this function
    to use this functionality

    e.g. you have to implement Simulation agent for interface
    when you create new one and you can not use existing
    """
    pass


def HwIO_walkSignals(hio: HwIOBase):
    if hio._hwIOs:
        for sHwIO in hio._hwIOs:
            yield from HwIO_walkSignals(sHwIO)
    else:
        yield hio


def HwIO_connectPacked(srcPacked: RtlSignalBase, dstInterface, exclude=None):
    """
    Connect 1D vector signal to this structuralized interface
    (LSB of first interface is LSB of result)

    :param packedSrc: vector which should be connected
    :param dstInterface: structuralized interface where should
        packedSrc be connected to
    :param exclude: sub interfaces of self which should be excluded
    """
    offset = 0
    connections = []
    for i in list(HwIO_walkSignals(dstInterface)):
        if exclude is not None and i in exclude:
            continue
        sig = i._sig
        t = sig._dtype
        w = t.bit_length()
        if w == 1:
            if srcPacked._dtype.bit_length() == 1:
                assert offset == 0, srcPacked
                s = srcPacked
            else:
                s = srcPacked[offset]
            offset += 1
        else:
            assert srcPacked._dtype.bit_length() >= w + offset, ("Insufficient amount of bits in srcPacked", srcPacked, w, offset)
            s = srcPacked[(w + offset): offset]  # src is likely to have insufficient amount of bits
            offset += w

        assert sig._dtype.bit_length() == s._dtype.bit_length(), (sig, s, sig._dtype, s._dtype)
        connections.append(sig(s._reinterpret_cast(sig._dtype)))

    return connections


def HwIO_walkFlatten(hio: HwIOBase, shouldEnterHwIOFn):
    """
    :param shouldEnterHwIOFn: function (actual hio)
        returns tuple (shouldEnter, shouldYield)
    """
    _shouldEnter, _shouldYield = shouldEnterHwIOFn(hio)
    if _shouldYield:
        yield hio

    if shouldEnterHwIOFn:
        for sHwIO in hio._hwIOs:
            yield from HwIO_walkFlatten(sHwIO, shouldEnterHwIOFn)


def HwIO_pack(hio: HwIOBase, masterDirEqTo=DIRECTION.OUT, exclude=None) -> Union[HBitsConst, RtlSignalBase[HBits]]:
    """
    Concatenate all signals to one big signal, recursively
    (LSB of first interface is LSB of result)

    :param masterDirEqTo: only signals with this direction are packed
    :param exclude: sequence of signals/interfaces to exclude
    """
    if not hio._hwIOs:
        if hio._masterDir == masterDirEqTo:
            return hio._sig
        return None

    res = None
    for sHwIO in hio._hwIOs:
        if exclude is not None and sHwIO in exclude:
            continue

        if sHwIO._hwIOs:
            if sHwIO._masterDir == DIRECTION.IN:
                d = DIRECTION.opposite(masterDirEqTo)
            else:
                d = masterDirEqTo
            s = HwIO_pack(sHwIO, masterDirEqTo=d, exclude=exclude)
        else:
            if sHwIO._masterDir == masterDirEqTo:
                s = sHwIO._sig
            else:
                s = None

        if s is not None:
            if not isinstance(s._dtype, HBits) or  s._dtype.signed is not None:
                s = s._reinterpret_cast(HBits(s._dtype.bit_length()))

            if res is None:
                res = s
            else:
                res = s._concat(res)

    return res
