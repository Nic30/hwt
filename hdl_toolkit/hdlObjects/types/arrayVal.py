from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.types.defs import BOOL, INT
from hdl_toolkit.synthetisator.param import evalParam
from hdl_toolkit.hdlObjects.types.slice import Slice
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps


class ArrayVal(Value):
    
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
                if isinstance(v, RtlSignalBase): # is signal
                    assert v._dtype == typeObj.elmType
                    e = v
                else:
                    e = typeObj.elmType.fromPy(v)
                elements.append(e)
        
        
        return cls(elements, typeObj, val is not None)
    
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
            
        # [TODO] eventmask should be shared for all items
        # [TODO] dirty flag is required
        if iamVal and isinstance(key, Value):
            return self.val[key.val]
        
        
        return Operator.withRes(AllOps.INDEX, [self, key], self._dtype.elmType)
    
    def _eq(self, other):
        assert self._dtype.elmType == other._dtype.elmType
        assert self._dtype.size == other._dtype.size
        
        eq = True
        first = self.val[0]
        vld = first.vldMask
        ev = first.eventMask
        
        for a, b in zip(self.val, other.val):
            eq = eq and a == b
            vld = vld & a.vldMask & b.vldMask
            ev = ev & a.eventMask & b.eventMask
        return BOOL.getValueCls()(eq, BOOL, vld, eventMask=ev)
