from typing import TypeVar, Generic, Union

from hwt.hdl.types.hdlType import HdlType

T = TypeVar("T", bound=HdlType)


class RtlSignalBase(Generic[T]):
    """
    Main base class for all rtl signals
    """
    pass


class HwIOBase():
    """
    Main base class for all interfaces
    """
    pass


class HwModuleBase():
    """
    Main base class for all units
    """
    pass


HwModuleOrHwIOBase = Union[HwModuleBase, HwIOBase]
