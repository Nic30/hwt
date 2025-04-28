
from typing import Optional, Any, Union

from hwt.hdl.const import HConst
from hwt.hdl.types.defs import INT, STR, BOOL, SLICE, FLOAT64
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.variables import HdlSignalItem
from hwt.mainBases import HwIOBase, RtlSignalBase


defaultPyConversions = {
    int: INT,
    str: STR,
    bool: BOOL,
    slice: SLICE,
    float: FLOAT64
}


def toHVal(op: Any, suggestedType: Optional[HdlType]=None) -> Union[HConst, RtlSignalBase, HwIOBase]:
    """Convert python or hdl HConst/RtlSignal object to hdl HConst/RtlSignal object"""
    if isinstance(op, (HConst, HdlSignalItem)):
        return op
    elif isinstance(op, HwIOBase):
        sig = getattr(op, "_sig", None)
        if sig is not None:
            return sig
        else:
            return op
    else:
        if suggestedType is not None:
            return suggestedType.from_py(op)

        if isinstance(op, int):
            if op >= 1 << 31:
                raise TypeError(
                    f"Number {op:d} is too big to fit in 32 bit integer of HDL"
                    " use Bits type instead")
            elif op < -(1 << 31):
                raise TypeError(
                    f"Number {op:d} is too small to fit in 32 bit integer"
                    " of HDL use Bits type instead")

        try:
            hType = defaultPyConversions[type(op)]
        except KeyError:
            hType = None

        if hType is None:
            raise TypeError(f"Unknown hardware type for instance of {op.__class__}")

        return hType.from_py(op)
