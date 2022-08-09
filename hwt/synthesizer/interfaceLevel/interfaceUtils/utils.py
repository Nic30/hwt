from typing import Union

from hwt.hdl.constants import DIRECTION
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.defs import BIT
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class NotSpecified(Exception):
    """
    This error means that you need to implement this function
    to use this functionality

    e.g. you have to implement Simulation agent for interface
    when you create new one and you can not use existing
    """
    pass


def walkPhysInterfaces(intf):
    if intf._interfaces:
        for si in intf._interfaces:
            yield from walkPhysInterfaces(si)
    else:
        yield intf


def connectPacked(srcPacked, dstInterface, exclude=None):
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
    for i in list(walkPhysInterfaces(dstInterface)):
        if exclude is not None and i in exclude:
            continue
        sig = i._sig
        t = sig._dtype
        w = t.bit_length()
        if w == 1:
            if srcPacked._dtype.bit_length() == 1:
                s = srcPacked
            else:
                s = srcPacked[offset]
            offset += 1
        else:
            s = srcPacked[(w + offset): offset]
            offset += w
        connections.append(sig(s))

    return connections


def walkFlatten(interface, shouldEnterIntfFn):
    """
    :param shouldEnterIntfFn: function (actual interface)
        returns tuple (shouldEnter, shouldYield)
    """
    _shouldEnter, _shouldYield = shouldEnterIntfFn(interface)
    if _shouldYield:
        yield interface

    if shouldEnterIntfFn:
        for intf in interface._interfaces:
            yield from walkFlatten(intf, shouldEnterIntfFn)


def packIntf(intf, masterDirEqTo=DIRECTION.OUT, exclude=None) -> Union[BitsVal, RtlSignalBase[Bits]]:
    """
    Concatenate all signals to one big signal, recursively
    (LSB of first interface is LSB of result)

    :param masterDirEqTo: only signals with this direction are packed
    :param exclude: sequence of signals/interfaces to exclude
    """
    if not intf._interfaces:
        if intf._masterDir == masterDirEqTo:
            return intf._sig
        return None

    res = None
    for i in intf._interfaces:
        if exclude is not None and i in exclude:
            continue

        if i._interfaces:
            if i._masterDir == DIRECTION.IN:
                d = DIRECTION.opposite(masterDirEqTo)
            else:
                d = masterDirEqTo
            s = packIntf(i, masterDirEqTo=d, exclude=exclude)
        else:
            if i._masterDir == masterDirEqTo:
                s = i._sig
            else:
                s = None

        if s is not None:
            if res is None:
                res = s._reinterpret_cast(Bits(s._dtype.bit_length()))
            else:
                res = s._concat(res)

    return res
