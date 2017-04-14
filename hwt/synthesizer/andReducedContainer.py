
class AndReducedContainer(list):
    """
    Container of and terms usually used as container for condition
    """
    def __init__(self):
        super(AndReducedContainer, self).__init__()
        self.__s = set()

    def add(self, item):
        if item in self.__s:
            return False
        else:
            self.__s.add(item)
            list.append(self, item)
            return True

    def update(self, other):
        assert isinstance(other, AndReducedContainer)
        for i in other:
            self.add(i)

    def __contains__(self, key):
        return key in self.__s
