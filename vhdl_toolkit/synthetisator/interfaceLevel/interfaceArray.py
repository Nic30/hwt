from python_toolkit.arrayQuery import extendLen
from vhdl_toolkit.hdlObjects.vectorUtils import getWidthExpr
from vhdl_toolkit.hdlObjects.operatorDefs import AllOps

def forAllPhysInterfaces(intf):
    if intf._subInterfaces:
        for _, si in intf._subInterfaces.items():
            yield from forAllPhysInterfaces(si)
    else:
        yield intf

def forAllParams(intf, discovered=None):
    if discovered is None:
        discovered = set()
    
    for _, si in intf._subInterfaces.items():
        yield from forAllParams(si, discovered)
        
    for _, p in intf._params.items():
        if p not in discovered:
            discovered.add(p)
            yield p 
        
        

def splitToTermSet(width):
    try:
        width = width.singleDriver()
    except AttributeError:
        return set([width])
    assert(width.operator == AllOps.MUL)
    return set(width.ops)


class InterfaceArray():
    def __init__(self):
        self._arrayElemCache = []
        
    def _setMultipliedBy(self, factor):
        self._multipliedBy = factor
        for _, i in self._subInterfaces.items():
            i._setMultipliedBy(factor)
            
    def _tryExtractMultiplicationFactor(self):
        widths = []
        # collect all widths    
        for i in forAllPhysInterfaces(self):
            try:
                i._dtype.constrain
            except AttributeError:
                # if is not constrained vector this can not be a interfaceArray
                return 
            w = getWidthExpr(i._dtype)
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
    
    def __getitem__(self, index):
        if index < self._multipliedBy.staticEval().val:
            try:
                return self._arrayElemCache[index]
            except IndexError:
                extendLen(self._arrayElemCache, index + 1)
                e = self._mkElemItem()
                e._name = "%d" % index
                e._parent = self
                self._arrayElemCache[index] = e
                return e
        else:
            raise IndexError()
    
    def _mkElemItem(self):
        e = self.__class__()
        for pName, p in self._params.items():
            pToReplace = e._params[pName]
            e._replaceParam(e, pName, pToReplace)
        return e 
        
