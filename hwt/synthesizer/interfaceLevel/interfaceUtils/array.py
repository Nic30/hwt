from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy


class InterfaceArray():
    """
    Interface with multiplied widths of signals to create array of interfaces

    :ivar _arrayElemCache: list of elements in this interface array
    """
    def __init__(self):
        self._arrayElemCache = None

    def __len__(self):
        return int(self._asArraySize)

    def _initArrayItems(self):
        "instantiate my items into _arrayElemCache"
        self._arrayElemCache = []
        wm = int(self._widthMultiplier) // int(self._asArraySize)
        for index in range(len(self)):
            e = InterfaceProxy(self, index, index, None, wm)
            self._arrayElemCache.append(e)

    def _isInterfaceArray(self):
        return self._asArraySize is not None

    def __getitem__(self, key):
        try:
            return self._arrayElemCache[key]
        except IndexError as e:
            if not self._isInterfaceArray():
                raise IntfLvlConfErr("interface %s is not array and can not be indexed on" % self._name)
            else:
                raise e
        except TypeError:
            raise TypeError("Interface is not an array")
