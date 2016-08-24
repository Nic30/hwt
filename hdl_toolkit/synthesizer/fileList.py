

class FileList(list):
    def __init__(self, *args, **kwargs):
        super(FileList, self).__init__(*args, **kwargs)
        self.__s = set()
    
    def append(self, item):
        if item in self.__s:
            return False
        else:
            self.__s.add(item)
            list.append(self, item)
            return True
