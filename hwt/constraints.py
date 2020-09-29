from copy import copy
from typing import Union, Tuple

from hwt.synthesizer.interface import Interface
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.unit import Unit
from hwt.synthesizer.componentPath import ComponentPath


class iHdlConstrain():

    def _get_parent(self) -> Unit:
        raise NotImplementedError(self)

    def _copy_with_root_upadate(self, old_path_prefix, new_path_prefix):
        raise NotImplementedError()

    def register_on_parent(self):
        self._get_parent()._constraints.append(self)


def _get_parent_unit(path: Tuple[Union[Unit, Interface, RtlSignal, iHdlConstrain], ...]) -> Unit:
    """
    Search parent Unit instance in path
    """
    if isinstance(path, iHdlConstrain):
        return path._get_parent()

    for o in reversed(path):
        if isinstance(o, Unit):
            return o

    raise AssertionError("No parent unit in path", path)


def _get_absolute_path(obj) -> Union[Tuple[Union[Unit, Interface, RtlSignal, iHdlConstrain], ...], None]:
    """
    Get tuple containing a path of objects from top to this object
    """
    if obj is None:
        return None
    elif isinstance(obj, iHdlConstrain):
        return obj

    return ComponentPath(obj).resolve()


def _apply_path_update(path: ComponentPath, old_path_prefix: ComponentPath, new_path_prefix: ComponentPath):
    """
    Update prefix of the path tuple
    """
    if isinstance(path, iHdlConstrain):
        return path._copy_with_root_upadate(old_path_prefix, new_path_prefix)
    return path.update_prefix(old_path_prefix, new_path_prefix)


class set_max_delay(iHdlConstrain):
    """
    Object which represents the max_delay constrain

    * usually used to set propagation time between two clock domains etc.

    :ivar ~.start: start of the signal path
    :ivar ~.end: end of the signal path
    :ivar ~.time_ns: max delay of the specified path in ns
    """

    def __init__(self,
                 start: Union[Interface, RtlSignal],
                 end: Union[Interface, RtlSignal],
                 time_ns: float,
                 datapath_only=True,
                 ommit_registration=False):
        self.start = _get_absolute_path(start)
        self.end = _get_absolute_path(end)
        self.time_ns = time_ns
        self.datapath_only = datapath_only
        if not ommit_registration:
            self.register_on_parent()

    def _copy_with_root_upadate(self, old_path_prefix, new_path_prefix):
        new_o = copy(self)
        new_o.start = _apply_path_update(
            self.start, old_path_prefix, new_path_prefix)
        new_o.end = _apply_path_update(
            self.end, old_path_prefix, new_path_prefix)
        return new_o

    def _get_parent(self) -> Unit:
        return _get_parent_unit(self.end)


class set_false_path(iHdlConstrain):

    def __init__(self, start: Union[None, Interface, RtlSignal],
                 end: Union[None, Interface, RtlSignal],
                 ommit_registration=False):
        self.start = _get_absolute_path(start)
        self.end = _get_absolute_path(end)
        if not ommit_registration:
            self.register_on_parent()

    def _copy_with_root_upadate(self, old_path_prefix, new_path_prefix):
        return set_max_delay._copy_with_root_upadate(self, old_path_prefix, new_path_prefix)

    def _get_parent(self) -> Unit:
        o = self.start
        if o is None:
            o = self.end
        return _get_parent_unit(o)


class get_clock_of(iHdlConstrain):

    def __init__(self, obj: Union[Interface, RtlSignal],
                 ommit_registration=False):
        self.obj = _get_absolute_path(obj)

    def _copy_with_root_upadate(self, old_path_prefix, new_path_prefix):
        new_o = copy(self)
        new_o.obj = _apply_path_update(
            self.obj, old_path_prefix, new_path_prefix)
        return new_o

    def _get_parent(self) -> Unit:
        return _get_parent_unit(self.obj)


class set_async_reg(iHdlConstrain):
    """
    Placement constrain which tell that the register should be put as close as possible to it's src/dst

    It should not be placed on the FF on the src domain,
    but should be set on FFs (possibly more) on the destination domain.
    """

    def __init__(self, sig: RtlSignal,
                 ommit_registration=False):
        self.sig = _get_absolute_path(sig)
        if not ommit_registration:
            self.register_on_parent()

    def _copy_with_root_upadate(self, old_path_prefix, new_path_prefix):
        new_o = copy(self)
        new_o.sig = _apply_path_update(
            self.sig, old_path_prefix, new_path_prefix)
        return new_o

    def _get_parent(self) -> Unit:
        return _get_parent_unit(self.sig)
