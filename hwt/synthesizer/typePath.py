from copy import deepcopy
from typing import Union


class TypePath(tuple):
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

    def __copy__(self):
        return self.__class__(*self)

    def __deepcopy__(self, memo):
        res = self.__class__(*(deepcopy(x, memo) for x in self))
        memo[self] = res
        return res
