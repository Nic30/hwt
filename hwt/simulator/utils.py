from collections import deque
from inspect import isgenerator
import sys
from typing import Union, Sequence

from hwt.doc_markers import internal
from hwt.hwModule import HwModule
from hwt.hObjList import HObjList
from hwt.hdl.const import HConst
from hwt.hdl.types.arrayConst import HArrayConst
from hwt.mainBases import HwIOBase, HwModuleOrHwIOBase
from hwt.serializer.generic.indent import getIndent
from pyMathBitPrecise.bit_utils import ValidityError
from pyMathBitPrecise.bits3t import Bits3val


def pprintHwIO(hio: Union[HwModule, HwIOBase], indent:int=0, prefix:str="", file=sys.stdout):
    """
    Pretty print interface
    """
    try:
        s = hio._sig
    except AttributeError:
        s = None
    if s is None:
        s = ""
    else:
        s = " " + repr(s)

    file.write("".join([getIndent(indent), prefix, repr(hio._getFullName()),
                        s]))
    file.write("\n")

    if isinstance(hio, HObjList):
        for chHwIO, p in enumerate(hio):
            # interfaces have already name of this array and index in it's name
            pprintHwIO(p, indent=indent + 1, prefix=prefix, file=file)
    else:
        for chHwIO in hio._hwIOs:
            pprintHwIO(chHwIO, indent=indent + 1, file=file)


def pprintAgents(hwModuleOrHwIO: HwModuleOrHwIOBase, indent:int=0, prefix:str="", file=sys.stdout):
    if isinstance(hwModuleOrHwIO, HwIOBase):
        ag = hwModuleOrHwIO._ag
    elif isinstance(hwModuleOrHwIO, HObjList):
        for i, item in enumerate(hwModuleOrHwIO):
            item_prefix = f"{prefix}_{i:d}"
            pprintAgents(item, indent=indent + 1, prefix=item_prefix, file=file)
        return
    else:
        ag = None

    if ag is not None:
        indent_str = getIndent(indent)
        file.write(f"{indent_str:s}{prefix:s}{ag}\n")

    for hio in hwModuleOrHwIO._hwIOs:
        pprintAgents(hio, indent + 1, file=file)


@internal
def reconnectHwModuleSignalsToModel(synthesisedHwModuleOrHwIO: HwModuleOrHwIOBase, rtl_simulator):
    """
    Reconnect model signals to unit to run simulation with simulation model
    but use original unit interfaces for communication

    :param synthesisedHwModuleOrHwIO: interface where should be signals
        replaced from signals from modelCls
    :param rtl_simulator: RTL simulator form where signals
        for synthesisedHwModuleOrHwIO should be taken
    """
    obj = synthesisedHwModuleOrHwIO

    for hio in obj._hwIOs:
        if hio._hwIOs:
            reconnectHwModuleSignalsToModel(hio, rtl_simulator)
        else:
            # reconnect signal from model
            name = hio._sigInside.name
            # update name and dtype
            s = getattr(rtl_simulator.io, name)
            if s._dtype is None:
                s._dtype = hio._dtype
            s._name = hio._name
            s.name = name
            hio.read = s.read
            hio.write = s.write
            hio.wait = s.wait
            hio._sigInside = s


def HConstSequenceToInts(values: Sequence[HConst]):
    """
    Iterable of values to ints (nonvalid = None)
    """
    return [Bits3valToInt(d) for d in values]


def agentDataToInts(interface):
    """
    Convert all values which has agent collected in time >=0 to integer array.
    Invalid value will be None.
    """
    return HConstSequenceToInts(interface._ag.data)


def Bits3valToInt(v: HConst):
    try:
        return int(v)
    except ValidityError:
        return None


def allHConstsToInts(sequenceOrVal):
    """
    Convert HConst instances to int recursively (for sequences)
    """
    if isinstance(sequenceOrVal, HArrayConst):
        sequenceOrVal = sequenceOrVal.val

    if isinstance(sequenceOrVal, (HConst, Bits3val)):
        return Bits3valToInt(sequenceOrVal)
    elif not sequenceOrVal:
        return sequenceOrVal
    elif (isinstance(sequenceOrVal, (list, tuple, deque))
          or isgenerator(sequenceOrVal)):
        seq = []
        for i in sequenceOrVal:
            seq.append(allHConstsToInts(i))

        if isinstance(sequenceOrVal, tuple):
            return tuple(seq)

        return seq
    else:
        return sequenceOrVal
