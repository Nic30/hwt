from copy import deepcopy
from typing import Union, SupportsIndex, Self


class TypePath(tuple[Union[str, int], ...]):
    """
    A path in hierarchy of structuralized type
    """

    def __new__ (cls, *objs):
        return super(TypePath, cls).__new__(cls, objs)

    def __truediv__(self, other: Union[int, str, "TypePath"]):
        if isinstance(other, TypePath):
            return TypePath(*self, *other)
        else:
            assert isinstance(other, (int, str)), other
            return TypePath(*self, other)

    def getOnObject(self, o):
        for n in self:
            if isinstance(n, int):
                o = o[n]
            else:
                assert isinstance(n, str), n
                o = getattr(o, n)
        return o

    def __getitem__(self, key:SupportsIndex)->Union[Self, int, str]:
        if isinstance(key, int):
            return tuple.__getitem__(self, key)
        else:
            return TypePath(*tuple.__getitem__(self, key))
            
    def setOnObject(self, o, newV):
        assert self
        o = self[:-1].getOnObject(o)
        n = self[-1]
        if isinstance(n, int):
            o[n] = newV
        else:
            assert isinstance(n, str), n
            setattr(o, n, newV)

    def __copy__(self):
        return self.__class__(*self)

    def __deepcopy__(self, memo):
        res = self.__class__(*(deepcopy(x, memo) for x in self))
        memo[self] = res
        return res
