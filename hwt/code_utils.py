from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.types.defs import BIT
from hwt.hdl.value import HValue
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from ipCorePackager.constants import DIRECTION


def rename_signal(unit_instance: "Unit",
                  sig: Union[RtlSignalBase, int, bool],
                  name: str):
    """
    Wrap signal or value in signal of specified name

    :attention: output signal is driven by new signal of a specified name
        this means that the assigning to a new signal does not drive a original signal
    """

    if isinstance(sig, (int, bool)):
        t = BIT
    else:
        t = sig._dtype

    if isinstance(sig, (HValue, int, bool)):
        s = unit_instance._sig(name, t, def_val=sig, nop_val=sig)
    else:
        s = unit_instance._sig(name, t)
        s(sig)

    return s


def connect_optional(src: InterfaceBase, dst: InterfaceBase,
                     check_fn=lambda intf_a, intf_b: (True, [])):
    """
    Connect interfaces and ignore all missing things

    :param check_fn: filter function(intf_a, intf_b) which check if interfaces should be connected
        returns tuple (do_check, extra_connection_list)
    """
    return list(_connect_optional(src, dst, check_fn, False))


@internal
def _connect_optional(src: InterfaceBase, dst: InterfaceBase, check_fn, dir_reverse):
    do_connect, extra_connections = check_fn(src, dst)
    yield from extra_connections
    if not do_connect:
        return

    if not src._interfaces:
        assert not dst._interfaces, (src, dst)
        if dir_reverse:
            yield src(dst)
        else:
            yield dst(src)

    for _s in src._interfaces:
        _d = getattr(dst, _s._name, None)
        if _d is None:
            # if the interfaces does not have subinterface of same name
            continue

        if _d._masterDir == DIRECTION.IN:
            rev = not dir_reverse
        else:
            rev = dir_reverse

        yield from _connect_optional(_s, _d, check_fn, rev)


@internal
def _intfToSig(obj):
    if isinstance(obj, InterfaceBase):
        return obj._sig
    else:
        return obj


@internal
def _mkOp(fn):
    """
    Function to create variadic operator function

    :param fn: function to perform binary operation
    """

    def op(*operands, key=None) -> RtlSignalBase:
        """
        :param operands: variadic parameter of input uperands
        :param key: optional function applied on every operand
            before processing
        """
        assert operands, operands
        top = None
        if key is not None:
            operands = map(key, operands)

        for s in operands:
            if top is None:
                top = s
            else:
                top = fn(top, s)
        return top

    return op

