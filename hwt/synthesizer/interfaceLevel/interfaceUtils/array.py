from hwt.hdlObjects.constants import INTF_DIRECTION
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.pyUtils.arrayQuery import arr_any
from hwt.synthesizer.exceptions import IntfLvlConfErr
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces
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

    def _setMultipliedBy(self, factor, updateTypes=True):
        self._multipliedBy = factor
        for i in self._interfaces:
            i._setMultipliedBy(factor, updateTypes=updateTypes)

    def __len__(self):
        return self._multipliedBy

    def _initArrayItems(self):
        "instantiate my items into _arrayElemCache"
        self._arrayElemCache = []
        for index in range(self._multipliedBy.staticEval().val):
            e = self._mkElemItem()
            e._name = "%d" % index
            e._parent = self
            e._isExtern = self._isExtern
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

    def _connectMyElems(self):
        if self._arrayElemCache:
            for indx, e in enumerate(self._arrayElemCache):
                elemHasConnections = arr_any(walkPhysInterfaces(e),
                                             lambda x: (bool(x._sig.endpoints) or
                                                        bool(x._sig.drivers)))
                if elemHasConnections:
                    e._resolveDirections()

                    if e._direction == INTF_DIRECTION.MASTER:
                        e._connectTo(self, masterIndex=indx)
                    else:
                        self._connectTo(e, slaveIndex=indx)

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
