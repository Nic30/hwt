

class UniqList(list):
    """
    List of unique items
    """

    def __init__(self, initSeq=None):
        super(UniqList, self).__init__()
        self.__s = set()
        if initSeq is not None:
            for item in initSeq:
                self.append(item)

    def append(self, item):
        if item in self.__s:
            return False
        else:
            self.__s.add(item)
            list.append(self, item)
            return True

    def extend(self, items):
        for item in items:
            self.append(item)

    def insert(self, i, x):
        super(UniqList, self).insert(i, x)
        self.__s.add(x)

    def _get_set(self):
        return self.__s

    def intersection_set(self, other):
        return self.__s.intersection(other._get_set())

    def discard(self, item):
        if item in self.__s:
            self.remove(item)
            return True
        else:
            return False

    def remove(self, item):
        self.__s.remove(item)
        return list.remove(self, item)

    def pop(self, *args, **kwargs):
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

    def __contains__(self, key):
        return key in self.__s
