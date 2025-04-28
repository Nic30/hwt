from copy import deepcopy

from hwt.hwIO import HwIO
from hwt.hwModule import HwModule
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


def to_tuple_of_names(objs):
    res = []
    for o in objs:
        name = getattr(o, "_name", None)
        if name is None:
            name = repr(o)
        res.append(name)
    return tuple(res)


class ComponentPath(tuple):

    def __new__ (cls, *objs):
        return super(ComponentPath, cls).__new__(cls, objs)

    def __truediv__(self, other):
        if isinstance(other, ComponentPath):
            return ComponentPath(*self, *other)
        else:
            return ComponentPath(*self, other)

    def resolve(self) -> "ComponentPath":
        """
        Make the path absolute

        The ComponentPath is in absolute format only if:

        * The first member is a top component or path is empty
        * All members except the last are :class:`hwt.hwModule.HwModule` instances (last can be RtlSignal/HwIO)
        * Each successor member is instantiated in predecessor except for :class:`hwt.hwModule.HwModule` instance with shared component
        * If member is a :class:`hwt.hwModule.HwModule` instance with shared component the successor must be an interface of this instance or an object from shared component
        """
        it = iter(reversed(self))
        try:
            obj = next(it)
        except StopIteration:
            # empty path
            return self

        path = []
        while obj is not None:
            _handle = next(it, None)
            if isinstance(_handle, HwModule) and _handle._shared_component_with is not None:
                handle, _, _ = _handle._shared_component_with
            else:
                handle = _handle

            if obj is not handle:
                if isinstance(obj, RtlSignal):
                    # to not modify path if it is already in absolute format
                    if not path or path[-1] is not obj:
                        path.append(obj)
                    obj = obj._rtlCtx.parent

                while isinstance(obj, HwIO):
                    if not path:
                        path.append(obj)
                    if obj is handle:
                        break
                    obj = obj._parent

                while obj is not handle:
                    assert isinstance(obj, HwModule), obj
                    # to not modify path if it is already in absolute format
                    if not path or path[-1] is not obj:
                        path.append(obj)

                    obj = obj._parent

            obj = _handle

        return ComponentPath(*reversed(path))

    def is_absolute(self):
        """
        :return: True if path starts with a top component else False
        """
        m = self[0]
        return isinstance(m, HwModule) and m._parent is None

    def update_prefix(self, old_path_prefix: "ComponentPath", new_path_prefix: "ComponentPath"):
        """
        Update prefix of the path tuple
        """
        assert len(self) >= len(old_path_prefix), (self, old_path_prefix)
        for p, op in zip(self, old_path_prefix):
            assert p is op, (self, old_path_prefix)

        return ComponentPath(*new_path_prefix, *self[len(old_path_prefix):])

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(*tuple.__getitem__(self, key))
        else:
            return tuple.__getitem__(self, key)

    def __repr__(self):
        return f"<{self.__class__.__name__:s} {str(self):s}>"

    def __str__(self):
        return "/".join(to_tuple_of_names(self))

    def __copy__(self):
        return self.__class__(*self)

    def __deepcopy__(self, memo):
        res = self.__class__(*(deepcopy(x, memo) for x in self))
        memo[self] = res
        return res
