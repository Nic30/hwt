from typing import Union

from hwt.synthesizer.interface import Interface
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.unit import Unit


def get_parent_unit(obj) -> Unit:
    if isinstance(obj, ConstrainBase):
        return obj.get_parent()

    while not isinstance(obj, Unit):
        if isinstance(obj, RtlSignal):
            obj = obj.ctx.parent
        else:
            obj = obj._parent
    return obj


class ConstrainBase():

    def get_parent(self) -> Unit:
        raise NotImplementedError(self)

    def register_on_parent(self):
        self.get_parent()._constraints.append(self)
    
class set_max_delay(ConstrainBase):
    """
    Object which represents the max_delay constrain

    * usually used to set propagation time between two clock domains etc.

    :ivar start: start of the signal path
    :ivar end: end of the signal path
    :ivar time_ns: max delay of the specified path in ns
    """

    def __init__(self,
                 start: Union[Interface, RtlSignal],
                 end: Union[Interface, RtlSignal],
                 time_ns: float,
                 datapath_only=True):
        self.start = start
        self.end = end
        self.time_ns = time_ns
        self.datapath_only = datapath_only
        self.register_on_parent()

    def get_parent(self) -> Unit:
        return get_parent_unit(self.end)

class set_false_path(ConstrainBase):
    def __init__(self, start: Union[None, Interface, RtlSignal], end: Union[None, Interface, RtlSignal]):
        self.start = start
        self.end = end
        self.register_on_parent()

    def get_parent(self)->Unit:
        o = self.start
        if o is None:
            o = self.end
        return get_parent_unit(o)

class get_clock_of(ConstrainBase):
    def __init__(self, obj):
        self.obj = obj

    def get_parent(self)->Unit:
        return get_parent_unit(self.obj)


class set_async_reg(ConstrainBase):
    """
    Placement constrain which tell that the register should be put as close as possible to it's src/dst

    It should not be placed on the FF on the src domain,
    but should be set on FFs (possibly more) on the destination domain.
    """

    def __init__(self, sig: RtlSignal):
        self.sig = sig
        self.register_on_parent()

    def get_parent(self)->Unit:
        return get_parent_unit(self.sig)
