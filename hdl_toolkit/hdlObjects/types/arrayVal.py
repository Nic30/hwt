from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.types.defs import BOOL, INT
from hdl_toolkit.hdlObjects.types.slice import Slice
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.synthesizer.param import evalParam
from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlSignalBase

class ArrayVal(Value):
    """
    Class of value of array
    """
    
    @classmethod
    def fromPy(cls, val, typeObj):
        size = evalParam(typeObj.size)
        if isinstance(size, Value):
            size = size.val
        
        if val is None:
            v = typeObj.elmType.fromPy(None)
            elements = [v.clone() for _ in range(size)]
        else:
            elements = []
            for v in val:
                if isinstance(v, RtlSignalBase):  # is signal
                    assert v._dtype == typeObj.elmType
                    e = v
                else:
                    e = typeObj.elmType.fromPy(v)
                elements.append(e)
        
        
        return cls(elements, typeObj, int(val is not None))
    
    def __getitem__(self, key):
        iamVal = isinstance(self, Value)
        key = toHVal(key)
        isSLICE = isinstance(key, Slice.getValueCls())
        
        if isSLICE:
            raise NotImplementedError()
        elif isinstance(key, RtlSignalBase):
            key = key._convert(INT)
        elif isinstance(key, Value):
            pass
        else:
            raise NotImplementedError("Index operation not implemented for index %s" % 
                                       (repr(key)))
            
        if iamVal and isinstance(key, Value):
            v = self.val[key.val].clone()
            if not key._isFullVld():
                v.vldMask = 0
            
            return v
        
        return Operator.withRes(AllOps.INDEX, [self, key], self._dtype.elmType)
    
    def __setitem__(self, index, value):
        assert isinstance(self, Value)
        assert index._dtype == INT, index._dtype 
        
        self.updateTime = max(index.updateTime, value.updateTime)
        if index._isFullVld():
            self.val[index.val] = value.clone()
        else:
            for v in self.val:
                v.vldMask = 0 
                v.updateTime = self.updateTime
            self.vldMask = 0
    
    def _eq(self, other):
        assert self._dtype.elmType == other._dtype.elmType
        assert self._dtype.size == other._dtype.size
        
        eq = True
        first = self.val[0]
        vld = first.vldMask
        updateTime = first.updateTime
        
        for a, b in zip(self.val, other.val):
            eq = eq and a == b
            vld = vld & a.vldMask & b.vldMask
            updateTime = max(updateTime, a.updateTime, b.updateTime)
        return BOOL.getValueCls()(eq, BOOL, vld, updateTime)
