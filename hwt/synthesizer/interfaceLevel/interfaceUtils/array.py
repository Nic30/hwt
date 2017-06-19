from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy
from hwt.synthesizer.param import evalParam


class InterfaceArray():
    """
    Interface with multiplied widths of signals to create array of interfaces

    :ivar _arrayElemCache: list of elements in this interface array
    """
    def __init__(self):
        self._arrayElemCache = None

    def __len__(self):
        return evalParam(self._asArraySize).val

    def _initArrayItems(self):
        "instantiate my items into _arrayElemCache"
        self._arrayElemCache = []
        wm = evalParam(self._widthMultiplier).val // evalParam(self._asArraySize).val
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

    def _mkElemItem(self):
        "create element for this interface array"
        e = self.__class__()
        e._updateParamsFrom(self)
        e._loadDeclarations()
        return e
