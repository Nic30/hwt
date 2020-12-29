from collections import deque
from inspect import isgenerator
import sys
from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.types.arrayVal import HArrayVal
from hwt.hdl.value import HValue
from hwt.serializer.generic.indent import getIndent
from hwt.synthesizer.hObjList import HObjList
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.unit import Unit
from pyMathBitPrecise.bits3t import Bits3val


def pprintInterface(intf: Union[Unit, InterfaceBase], indent:int=0, prefix:str="", file=sys.stdout):
    """
    Pretty print interface
    """
    try:
        s = intf._sig
    except AttributeError:
        s = None
    if s is None:
        s = ""
    else:
        s = " " + repr(s)

    file.write("".join([getIndent(indent), prefix, repr(intf._getFullName()),
                        s]))
    file.write("\n")

    if isinstance(intf, HObjList):
        for i, p in enumerate(intf):
            # interfaces have already name of this array and index in it's name
            pprintInterface(p, indent=indent + 1, prefix=prefix, file=file)
    else:
        for i in intf._interfaces:
            pprintInterface(i, indent=indent + 1, file=file)


def pprintAgents(unitOrIntf: Union[Unit, InterfaceBase], indent:int=0, prefix:str="", file=sys.stdout):
    if isinstance(unitOrIntf, InterfaceBase):
        ag = unitOrIntf._ag
    elif isinstance(unitOrIntf, HObjList):
        for i, item in enumerate(unitOrIntf):
            item_prefix = f"{prefix}_{i:d}"
            pprintAgents(item, indent=indent + 1, prefix=item_prefix, file=file)
        return
    else:
        ag = None

    if ag is not None:
        indent_str = getIndent(indent)
        file.write(f"{indent_str:s}{prefix:s}{ag}\n")

    for i in unitOrIntf._interfaces:
        pprintAgents(i, indent + 1, file=file)


@internal
def reconnectUnitSignalsToModel(synthesisedUnitOrIntf: Union[Unit, InterfaceBase], rtl_simulator):
    """
    Reconnect model signals to unit to run simulation with simulation model
    but use original unit interfaces for communication

    :param synthesisedUnitOrIntf: interface where should be signals
        replaced from signals from modelCls
    :param rtl_simulator: RTL simulator form where signals
        for synthesisedUnitOrIntf should be taken
    """
    obj = synthesisedUnitOrIntf

    for intf in obj._interfaces:
        if intf._interfaces:
            reconnectUnitSignalsToModel(intf, rtl_simulator)
        else:
            # reconnect signal from model
            name = intf._sigInside.name
            # update name and dtype
            s = getattr(rtl_simulator.io, name)
            if s._dtype is None:
                s._dtype = intf._dtype
            s._name = intf._name
            s.name = name
            intf.read = s.read
            intf.write = s.write
            intf.wait = s.wait
            intf._sigInside = s


def valuesToInts(values):
    """
    Iterable of values to ints (nonvalid = None)
    """
    return [valToInt(d) for d in values]


def valToInt(v):
    try:
        return int(v)
    except ValueError:
        return None

def allValuesToInts(sequenceOrVal):
    """
    Convert HValue instances to int recursively (for sequences)
    """
    if isinstance(sequenceOrVal, HArrayVal):
        sequenceOrVal = sequenceOrVal.val

    if isinstance(sequenceOrVal, (HValue, Bits3val)):
        return valToInt(sequenceOrVal)
    elif not sequenceOrVal:
        return sequenceOrVal
    elif (isinstance(sequenceOrVal, (list, tuple, deque))
          or isgenerator(sequenceOrVal)):
        seq = []
        for i in sequenceOrVal:
            seq.append(allValuesToInts(i))

        if isinstance(sequenceOrVal, tuple):
            return tuple(seq)

        return seq
    else:
        return sequenceOrVal
