

class UniqList(list):
    """
    List of unique items
    """

    def __init__(self):
        super(UniqList, self).__init__()
        self.__s = set()

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

    def pop(self, *args, **kwargs):
        item = list.pop(self, *args, **kwargs)
        self.__s.remove(item)
        return item

    def remove(self, item):
        self.__s.remove(item)
        return list.remove(self, item)

    def clear(self):
        list.clear(self)
        self.__s.clear()

    def copy(self):
        c = UniqList()
        c.extend(self)
        return c

    def __contains__(self, key):
        return key in self.__s
