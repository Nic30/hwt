from copy import deepcopy

from hwt.synthesizer.interface import Interface
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.unit import Unit


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
        """
        obj = self[0]
        path = []
        if isinstance(obj, RtlSignal):
            path.append(obj)
            obj = obj.ctx.parent
    
        while isinstance(obj, Interface):
            obj = obj._parent
    
        while obj is not None:
            path.append(obj)
            obj = obj._parent
    
        return ComponentPath(*reversed(path), *self[1:])
    
    def is_absolute(self):
        """
        :return: True if path starts with a top component else False
        """
        u = self[0]
        return isinstance(u, Unit) and u._parent is None

    def update_prefix(self, old_path_prefix: "ComponentPath", new_path_prefix: "ComponentPath"):
        """
        Update prefix of the path tuple
        """
        assert len(self) >= len(old_path_prefix), (self, old_path_prefix)
        for p, op in zip(self, old_path_prefix):
            assert p is op, (self, old_path_prefix)
    
        return ComponentPath(*new_path_prefix, *self[len(old_path_prefix):])

    def __copy__(self):
        return self.__class__(*self)

    def __deepcopy__(self, memo):
        res = self.__class__(*(deepcopy(x, memo) for x in self))
        memo[self] = res
        return res
