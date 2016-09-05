

class UniqList(list):
    """
    List of unique items
    """
    def __init__(self, *args, **kwargs):
        super(UniqList, self).__init__(*args, **kwargs)
        self.__s = set()
    
    def append(self, item):
        if item in self.__s:
            return False
        else:
            self.__s.add(item)
            list.append(self, item)
            return True
