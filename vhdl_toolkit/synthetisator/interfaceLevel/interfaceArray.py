from python_toolkit.arrayQuery import extendLen
from vhdl_toolkit.hdlObjects.vectorUtils import getWidthExpr

class InterfaceArray():
    def __init__(self):
        self._arrayElemCache = []
        
    def _setMultipliedBy(self, factor):
        self._multipliedBy = factor
        for _, i in self._subInterfaces.items():
            i._setMultipliedBy(factor)
            
    def _tryExtractMultiplicationFactor(self):
        def forAllPhysInterfaces(intf):
            if intf._subInterfaces:
                for _, si in intf._subInterfaces.items():
                    yield from forAllPhysInterfaces(si)
            else:
                yield intf
        
        widths = []
            
        for i in forAllPhysInterfaces(self):
            try:
                w = getWidthExpr(i._dtype)
            except AttributeError:
                return
            widths.append(w)
        def splitToTermSets(width):
            return width
        
        widths = map(splitToTermSets, widths)
        raise NotImplementedError()
    
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
        
