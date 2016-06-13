from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.hdlObjects.types.defs import BOOL, INT, BIT
from hdl_toolkit.hdlObjects.typeShortcuts import mkRange
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.slice import Slice
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase

BoolVal = BOOL.getValueCls()

def bitsCmp(self, other, op):
    """
    @attention: If other is Bool signal convert this to boolean (not ideal, due VHDL event operator)
    """
    other = toHVal(other)
    
    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value) 
    
    if iamVal and otherIsVal:
        w = self._dtype.bit_length()
        assert(w == other._dtype.bit_length())
        
        vld = self.vldMask & other.vldMask
        res = op._evalFn(self.val, other.val) and vld == Bitmask.mask(w)
        ev = self.eventMask | other.eventMask
    
        return BoolVal(res, BOOL, vld, eventMask=ev)
    else:
        if other._dtype == BOOL:
            self = self._convert(BOOL)
        elif self._dtype == other._dtype:
            pass
        else:
            raise NotImplementedError("Types are not comparable (%s, %s)" % (repr(self._dtype), repr(other._dtype)))
        
        return Operator.withRes(op, [self, other], BOOL) 

def bitsBitOp(self, other, op):
    """
    @attention: If other is Bool signal convert this to boolean (not ideal, due VHDL event operator)
    """
    other = toHVal(other)
    
    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value) 
    
    if iamVal and otherIsVal:
        w = self._dtype.bit_length()
        assert(w == other._dtype.bit_length())
        
        vld = self.vldMask & other.vldMask
        res = op._evalFn(self.val, other.val) & vld
        ev = self.eventMask | other.eventMask
    
        return BoolVal(res, BOOL, vld, eventMask=ev)
    else:
        if other._dtype == BOOL:
            self = self._convert(BOOL)
        elif self._dtype == other._dtype:
            pass
        else:
            raise NotImplementedError("Types are not comparable (%s, %s)" % (repr(self._dtype), repr(other._dtype)))
        
        return Operator.withRes(op, [self, other], self._dtype) 


class BitsVal(Value):
    """
    @attention: operator on signals are using value operator functions as well 
    """
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
    
    # [TODO] bit reverse operator
    
    def _concat(self, other):
        w = self._dtype.bit_length()
        resWidth = w + other._dtype.bit_length()
        resT = mkRange(resWidth - 1, 0)
        
        if isinstance(self, Value) and isinstance(other, Value):
            v = self.clone()
            v.val = (v.val << w) | other.val
            v.vldMask = (v.vldMask << w) | other.vldMask
            v.eventMask = (v.eventMask << w) | other.eventMask
            v._dtype = resT
            return v    
        else:
            # is instance of signal
            if isinstance(other, InterfaceBase):
                other = other._src
            return Operator.withRes(AllOps.CONCAT, [self, other], resT)
    
    def __getitem__(self, key):
        iamVal = isinstance(self, Value)
        st = self._dtype
        l = st.bit_length()
        if l == 1:
            assert(st.forceVector)  # assert not indexing on single bit
            
        # [TODO] what about Slice hdl class?
        # [TODO] boundary check
        if isinstance(key, slice):
            if key.step is not None or key.start is None or key.stop is None:
                raise NotImplementedError()
            stop = toHVal(key.stop)
            start = toHVal(key.start)

            isVal = iamVal and isinstance(start, Value) and isinstance(stop, Value) 
            if isVal:
                raise NotImplementedError("[TODO] bit select on value")
            else:
                key = (start - INT.fromPy(1))._downto(stop)
                resT = Bits(widthConstr=key, forceVector=True, signed=st.signed)
                
        elif isinstance(key, (int, Integer)):
            key = toHVal(key)
            resT = BIT
            
        elif isinstance(key, Signal):
            t = key._dtype
            if isinstance(t, Integer):
                resT = BIT
            elif isinstance(t, Slice):
                resT = Bits(widthConstr=key, forceVector=st.forceVector, signed=st.signed)
            elif isinstance(t, Bits):
                raise NotImplementedError("[TODO] bits to integer conversion while indexing")
            else:
                raise NotImplementedError("Index operation not implemented for index of type %s" % (repr(t)))
       
        else:
            raise NotImplementedError("Index operation not implemented for index %s" % (repr(key)))
            
        return Operator.withRes(AllOps.INDEX, [self, key], resT)


    # comparisons         
    
    def _eq(self, other):
        return bitsCmp(self, other, AllOps.EQ)
    
    def __ne__(self, other):
        return bitsCmp(self, other, AllOps.NEQ)
    
    def __lt__(self, other):
        return bitsCmp(self, other, AllOps.LOWERTHAN)
    
    def __gt__(self, other):
        return bitsCmp(self, other, AllOps.GREATERTHAN)
    
    def __ge__(self, other):
        return bitsCmp(self, other, AllOps.GE)
   
    def __le__(self, other):
        return bitsCmp(self, other, AllOps.LE)
    
    def __xor__(self, other):
        return bitsBitOp(self, other, AllOps.XOR)
    
    def __and__(self, other):
        return bitsBitOp(self, other, AllOps.AND_LOG)
    
    def __or__(self, other):
        return bitsBitOp(self, other, AllOps.OR_LOG)
       
    def _hasEvelnt(self):
        if isinstance(self, Value):
            return BoolVal(bool(self.eventMask), BOOL, self.vldMask, eventMask=self.eventMask)
        else:
            return Operator.withRes(AllOps.EVENT, [self], BOOL)
    
    def _onRisingEdge(self):
        if isinstance(self, Value):
            return BoolVal(bool(self.eventMask) and self.val, BOOL, self.vldMask, eventMask=self.eventMask)
        else:
            return Operator.withRes(AllOps.RISING_EDGE, [self], BOOL)
    
    
        
