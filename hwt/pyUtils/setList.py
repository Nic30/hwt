from typing import Generic, TypeVar, Set, Sequence, Optional

T = TypeVar('T')


class SetList(Generic[T], list):
    """
    List of unique items
    """
    __slots__ = ["__s"]

    def __init__(self, initSeq: Optional[Sequence[T]]=None):
        super(SetList, self).__init__()
        self.__s: Set[T] = set()
        if initSeq is not None:
            for item in initSeq:
                self.append(item)

    def append(self, item: T) -> bool:
        """
        :return: True if the item was newly added
        """
        if item in self.__s:
            return False
        else:
            self.__s.add(item)
            list.append(self, item)
            return True

    def extend(self, items: Sequence[T]):
        for item in items:
            self.append(item)

    def insert(self, i: int, x: T):
        super(SetList, self).insert(i, x)
        self.__s.add(x)

    def _get_set(self) -> Set[T]:
        return self.__s

    def intersection_set(self, other: Set[T]):
        return self.__s.intersection(other._get_set())

    def discard(self, item: T) -> bool:
        """
        :return: True if the item was previously in this list
        """
        if item in self.__s:
            self.remove(item)
            return True
        else:
            return False

    def remove(self, item: T):
        self.__s.remove(item)
        return list.remove(self, item)

    def pop(self, *args, **kwargs) -> T:
        item = list.pop(self, *args, **kwargs)
        self.__s.remove(item)
        return item

    def clear(self):
        list.clear(self)
        self.__s.clear()

    def copy(self):
        c = SetList()
        c.extend(self)
        return c

    def __setitem__(self, i: int, v: T):
        if isinstance(i, slice):
            for item in self[i]:
                self.__s.remove(item)
            v = SetList(v)
            list.__setitem__(self, i, v)
            self.__s.update(v)
            
        else:
            assert isinstance(i, int)
            cur = self[i]
            self.__s.remove(cur)
            list.__setitem__(self, i, v)
            self.__s.add(v)

    def __copy__(self):
        return self.copy()

    def __contains__(self, key) -> bool:
        return key in self.__s
