from typing import Union

from hwt.doc_markers import internal
from hwt.hdl.types.defs import BIT
from hwt.hdl.types.typeCast import toHVal
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.vectorUtils import fitTo


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

    s = unit_instance._sig(name, t)
    s(sig)
    return s


@internal
def _intfToSig(obj):
    if isinstance(obj, InterfaceBase):
        return obj._sig
    else:
        return obj


@internal
def _connect(src, dst, exclude, fit):
    # [TODO]: support for RtlSignals of struct type + interface with same signal structure
    if isinstance(src, InterfaceBase):
        if isinstance(dst, InterfaceBase):
            return dst._connectTo(src, exclude=exclude, fit=fit)
        src = src._sig

    assert not exclude, "this intf. is just a signal, excluded should be already processed in this state"
    if src is None:
        src = dst._dtype.from_py(None)
    else:
        src = toHVal(src)

    if fit:
        src = fitTo(src, dst)

    src = src._auto_cast(dst._dtype)

    return dst(src)


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
