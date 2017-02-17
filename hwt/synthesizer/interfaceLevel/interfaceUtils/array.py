from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.constants import INTF_DIRECTION
from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.synthesizer.vectorUtils import getWidthExpr
from hwt.pyUtils.arrayQuery import arr_any
from hwt.synthesizer.exceptions import IntfLvlConfErr


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
    """
    def __init__(self):
        self._arrayElemCache = []
        
    def _setMultipliedBy(self, factor, updateTypes=True):
        self._multipliedBy = factor
        for i in self._interfaces:
            i._setMultipliedBy(factor, updateTypes=updateTypes)
    
    def _tryExtractMultiplicationFactor(self):
        widths = []
        # collect all widths    
        for i in walkPhysInterfaces(self):
            if i._dtypeMatch or i._boundedEntityPort._dtype.constrain is None:
                # if is not constrained vector or type was resolved this can not be a interfaceArray
                return 
            w = getWidthExpr(i._boundedEntityPort._dtype)
            widths.append(w)
            
        # find what have all widths in common
        splitedWidths = map(splitToTermSet, widths)
        arrLen = None
        for w in splitedWidths:
            if arrLen is None:
                arrLen = w
            else:
                arrLen = arrLen.intersection(w)
        
        if len(arrLen) == 1:  # if is possible to determine arrLen
            return list(arrLen)[0] 
    
    def __len__(self):
        return self._multipliedBy
    
    def _initArrayItems(self):
        self._arrayElemCache = []
        for index in range(self._multipliedBy.staticEval().val):
            e = self._mkElemItem()
            e._name = "%d" % index
            e._parent = self
            e._isExtern = self._isExtern
            self._arrayElemCache.append(e)
    
    def _connectMyElems(self):
        if self._arrayElemCache: 
            for indx, e in enumerate(self._arrayElemCache):
                elemHasConnections = arr_any(walkPhysInterfaces(e),
                                             lambda x: bool(x._sig.endpoints) 
                                                       or bool(x._sig.drivers))
                if elemHasConnections:
                    e._resolveDirections()
                    
                    if e._direction == INTF_DIRECTION.MASTER:
                        e._connectTo(self, masterIndex=indx)
                    else:
                        self._connectTo(e, slaveIndex=indx)
        
    
    def __getitem__(self, key):
        if self._multipliedBy is None:
            raise IntfLvlConfErr("interface %s is not array and can not be indexe on" % self._name)
        return self._arrayElemCache[key]
    
    def _mkElemItem(self):
        e = self.__class__()
        e._updateParamsFrom(self)
        e._loadDeclarations()
        return e 
        
