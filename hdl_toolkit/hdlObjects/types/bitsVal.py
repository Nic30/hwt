from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.typeShortcuts import mkRange


BoolVal = BOOL.getValueCls()

class BitsVal(Value):
    
    def _convSign(self, signed):
        if self._dtype.signed == signed:
            return self
        else:
            raise NotImplementedError()
        
    def _signed(self):
        return self._convSign(True)
    
    def _unsigned(self):
        return self._convSign(False)
    
    def _vec(self):
        return self._convSign(None)
                
    @classmethod
    def fromPy(cls, val, typeObj):
        assert(isinstance(val, (int, bool)) or val is None)
        vld = 0 if val is None else Bitmask.mask(typeObj.bit_length())
        if not vld:
            val = 0
        return cls(val, typeObj, vld)
    
    def _concat(self, other):
        from hdl_toolkit.synthetisator.rtlLevel.signal import SignalNode, Signal
        from hdl_toolkit.hdlObjects.operatorDefs import AllOps
        from hdl_toolkit.hdlObjects.operator import Operator
        w = self._dtype.bit_length()
        resWidth = w + other._dtype.bit_length()
        if isinstance(other, Value):
            v = self.clone()
            v.val = (v.val << w) | other.val
            v.vldMask = (v.vldMask << w) | other.vldMask
            v.eventMask = (v.eventMask << w) | other.eventMask
            v._dtype = mkRange(resWidth - 1, 0)
            return v    
        else:
            # is instance of signal
            if not isinstance(other, Signal):
                other = other._src
            op = Operator(AllOps.CONCAT, [self, other])
            return SignalNode.resForOp(op)
         
    
    def _eq(self, other):
        assert(isinstance(other, Value))
        w = self._dtype.bit_length()
        assert(w == other._dtype.bit_length())
        
        vld = self.vldMask & other.vldMask
        eq = self.val == other.val and vld == Bitmask.mask(w)
        ev = self.eventMask | other.eventMask

        return BoolVal(eq, BOOL, vld, eventMask=ev)
