from typing import Generic, TypeVar, Set, Sequence, Optional

T = TypeVar('T')


class UniqList(Generic[T], list):
    """
    List of unique items
    """

    def __init__(self, initSeq: Optional[Sequence[T]]=None):
        super(UniqList, self).__init__()
        self.__s: Set[T] = set()
        if initSeq is not None:
            for item in initSeq:
                self.append(item)

    def append(self, item: T) -> bool:
        """
        :returns: True if the item was in list already
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
        super(UniqList, self).insert(i, x)
        self.__s.add(x)

    def _get_set(self) -> Set[T]:
        return self.__s

    def intersection_set(self, other: Set[T]):
        return self.__s.intersection(other._get_set())

    def discard(self, item: T) -> bool:
        """
        :returns: True if the item was in list already
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
        c = UniqList()
        c.extend(self)
        return c

    def __copy__(self):
        return self.copy()

    def __contains__(self, key) -> bool:
        return key in self.__s
