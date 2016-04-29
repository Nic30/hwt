from python_toolkit.arrayQuery import extendLen
from hdl_toolkit.hdlObjects.vectorUtils import getWidthExpr
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.synthetisator.interfaceLevel.interface.utils import walkPhysInterfaces

def splitToTermSet(width):
    try:
        width = width.singleDriver()
    except (AttributeError, AssertionError):
        return set([width])
    if width.operator == AllOps.DIV:
        pass
    assert(width.operator == AllOps.MUL)
    return set(width.ops)


class InterfaceArray():
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
            if i._dtypeMatch or i._originEntityPort.dtype.constrain is None:
                # if is not constrained vector or type was resolved this can not be a interfaceArray
                return 
            w = getWidthExpr(i._originEntityPort.dtype)
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
            self._arrayElemCache.append(e)
    
    def _connectMyElems(self):
        if self._src is not None or self._endpoints:
            # [TODO] assert no element is connected to anything
            pass
        else:
            if self._arrayElemCache: 
                for indx, e in enumerate(self._arrayElemCache):
                    # [TODO] find better way how to find out direction of elements
                    e._propagateConnection()
                    hasEp = len(e._endpoints) > 0
                    
                    if hasEp:
                        e._connectTo(self, masterIndex=indx)
                    else:
                        self._connectTo(e, slaveIndex=indx)
            
    
    def __getitem__(self, index):
        if index < self._multipliedBy.staticEval().val:
            return self._arrayElemCache[index]
        else:
            raise IndexError()
    
    def _mkElemItem(self):
        e = self.__class__()
        e._updateParamsFrom(self)
        e._loadDeclarations()
        return e 
        
