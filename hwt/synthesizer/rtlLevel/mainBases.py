from typing import TypeVar, Generic

from hwt.hdl.types.hdlType import HdlType

T = TypeVar("T", bound=HdlType)


class RtlSignalBase(Generic[T]):
    """
    Main base class for all rtl signals
    """
    pass


class RtlMemoryBase(RtlSignalBase):
    """
    Main base class for all rtl memories
    """
    pass
