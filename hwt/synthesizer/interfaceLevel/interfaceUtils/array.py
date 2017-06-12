from hwt.hdlObjects.operatorDefs import AllOps
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy
from hwt.synthesizer.param import evalParam
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc


def splitToTermSet(width):
    """
    try split width expression to multiplicands
    """
    try:
        width = width.singleDriver()
    except (AttributeError, MultipleDriversExc):
        return set([width])
    if width.operator == AllOps.DIV:
        pass
    assert width.operator == AllOps.MUL
    return set(width.ops)


class InterfaceArray():
    """
    Interface with multiplied widths of signals to create array of interfaces

    :ivar _arrayElemCache: list of elements in this interface array
    """
    def __init__(self):
        self._arrayElemCache = []

    def __len__(self):
        return evalParam(self._multipliedBy).val

    def _initArrayItems(self):
        "instantiate my items into _arrayElemCache"
        self._arrayElemCache = []
        for index in range(len(self)):
            e = InterfaceProxy(self, index, None)
            self._arrayElemCache.append(e)

    def _isInterfaceArray(self):
        """Check if this interface is array itself,
            _multipliedBy can be set by parent and does not necessary means that this is array interface 
        """
        mb = self._multipliedBy
        if mb is not None:
            try:
                return self._multipliedBy is not self._parent._multipliedBy
            except AttributeError:
                return True
        else:
            return False

    def __getitem__(self, key):
        if not self._isInterfaceArray():
            raise IntfLvlConfErr("interface %s is not array and can not be indexed on" % self._name)
        return self._arrayElemCache[key]

    def _mkElemItem(self):
        "create element for this interface array"
        e = self.__class__()
        e._updateParamsFrom(self)
        e._loadDeclarations()
        return e
