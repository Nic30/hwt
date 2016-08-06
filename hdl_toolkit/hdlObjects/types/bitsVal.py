from copy import copy

from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.defs import BOOL, INT, BIT, SLICE
from hdl_toolkit.hdlObjects.types.eventCapableVal import EventCapableVal
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.integerVal import IntegerVal
from hdl_toolkit.hdlObjects.types.slice import Slice
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.value import Value, areValues
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.synthetisator.rtlLevel.signalUtils.exceptions import MultipleDriversExc


BoolVal = BOOL.getValueCls()

def bitsCmp(self, other, op, evalFn=None):
    """
    @attention: If other is Bool signal convert this to boolean (not ideal, due VHDL event operator)
    """
    other = toHVal(other)
    
    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value) 

    if evalFn is None:
        evalFn = op._evalFn
    
    if iamVal and otherIsVal:
        w = self._dtype.bit_length()
        assert w == other._dtype.bit_length(), "%d, %d" % (w, other._dtype.bit_length())
        
        vld = self.vldMask & other.vldMask
        _vld = vld == Bitmask.mask(w)
        res = evalFn(self.val, other.val) and _vld
        updateTime = max(self.updateTime, other.updateTime)
    
        return BoolVal(res, BOOL, int(_vld), updateTime)
    else:
        if other._dtype == BOOL:
            self = self._convert(BOOL)
        elif self._dtype == other._dtype:
            pass
        elif isinstance(other._dtype, Integer):
            other = other._convert(self._dtype) 
        else:
            raise NotImplementedError("Types are not comparable (%s, %s)" % (repr(self._dtype), repr(other._dtype)))
        
        return Operator.withRes(op, [self, other], BOOL) 

def bitsBitOp(self, other, op):
    """
    @attention: If other is Bool signal, convert this to boolean (not ideal, due VHDL event operator)
    """
    other = toHVal(other)
    
    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value) 
    
    if iamVal and otherIsVal:
        w = self._dtype.bit_length()
        assert w == other._dtype.bit_length()
        
        vld = self.vldMask & other.vldMask
        res = op._evalFn(self.val, other.val) & vld
        updateTime = max(self.updateTime, other.updateTime)
    
        return self.__class__(res, self._dtype, vld, updateTime)
    else:
        if other._dtype == BOOL:
            self = self._convert(BOOL)
        elif self._dtype == other._dtype:
            pass
        else:
            raise NotImplementedError("Types are not comparable (%s, %s)" %
                                       (repr(self._dtype), repr(other._dtype)))
        
        return Operator.withRes(op, [self, other], self._dtype) 

def bitsArithOp(self, other, op):
    other = toHVal(other)
    assert isinstance(other._dtype, (Integer, Bits))
    if areValues(self, other):
        v = self.clone()
        v.val = op._evalFn(self.val, other.val)

        # [TODO] correct overflow detection for signed values
        w = v._dtype.bit_length()
        v.val &= Bitmask.mask(w)
        
        # [TODO] value check range
        if isinstance(other._dtype, Integer):
            if other.vldMask:
                v.vldMask = self.vldMask
            else:
                v.vldMask = 0  
        else:
            v.vldMask = self.vldMask & other.vldMask
        v.updateTime = max(self.updateTime, other.updateTime)
        return v
    else:
        resT = self._dtype
        if self._dtype.signed is None:
            self = self._unsigned()
        if isinstance(other._dtype, Bits) and other._dtype.signed is None:
            other = other._unsigned() 
        elif isinstance(other._dtype, Integer):
            pass
        else:
            raise NotImplementedError("%s %s %s" % (repr(self), repr(op) , repr(other)))
        
        o = Operator.withRes(op, [self, other], self._dtype)
        return o._convert(resT)

def boundryFromType(sigOrVal, boundaryIndex):
    c = sigOrVal._dtype.constrain
    if isinstance(c, Value):  # slice
        return c.val[boundaryIndex]
    else:  # downto / to
        return c.singleDriver().ops[boundaryIndex]

class BitsVal(EventCapableVal):
    """
    @attention: operator on signals are using value operator functions as well 
    """
    def _convSign(self, signed):
        if self._dtype.signed == signed:
            return self
        else:
            t = copy(self._dtype)
            t.signed = signed
            if isinstance(self, Value):
                selfSign = self._dtype.signed 
                v = self.clone()
                w = self._dtype.bit_length()
                msbVal = 1 << (w - 1)
                if selfSign and not signed:
                    if v.val < 0:
                        v.val += msbVal
                elif not selfSign and signed:
                    if v.val >= msbVal:
                        v.val -= (msbVal - 1)
                    
                return v
            else:
                if signed is None:
                    cnv = AllOps.BitsAsVec
                elif signed:
                    cnv = AllOps.BitsAsSigned
                else:
                    cnv = AllOps.BitsAsUnsigned
                
                return Operator.withRes(cnv, [self], t)
        
    def _signed(self):
        return self._convSign(True)
    
    def _unsigned(self):
        return self._convSign(False)
    
    def _vec(self):
        return self._convSign(None)
                
    @classmethod
    def fromPy(cls, val, typeObj):
        assert isinstance(val, (int, bool)) or val is None, val
        vld = 0 if val is None else Bitmask.mask(typeObj.bit_length())
        if not vld:
            val = 0
        return cls(int(val), typeObj, vld)
    
    # [TODO] bit reverse operator
    def _concat(self, other):
        w = self._dtype.bit_length()
        other_w = other._dtype.bit_length()
        resWidth = w + other_w
        resT = vecT(resWidth)
        
        if isinstance(self, Value) and isinstance(other, Value):
            v = self.clone()
            v.val = (v.val << other_w) | other.val
            v.vldMask = (v.vldMask << other_w) | other.vldMask
            v.updateTime = max(self.updateTime, other.updateTime)
            v._dtype = resT
            return v    
        else:
            # is instance of signal
            if isinstance(other, InterfaceBase):
                other = other._sig
            return Operator.withRes(AllOps.CONCAT, [self, other], resT)
    
    def __getitem__(self, key):
        iamVal = isinstance(self, Value)
        st = self._dtype
        l = st.bit_length()
        if l == 1:
            assert st.forceVector  # assert not indexing on single bit
            
        # [TODO] boundary check
        isSlice = isinstance(key, slice)
        isSLICE = isinstance(key, Slice.getValueCls())
        if areValues(self, key):
            updateTime = max(self.updateTime, key.updateTime)
            keyVld = key._isFullVld() 
            val = 0
            vld = 0
            
            if key._dtype == INT:
                if keyVld:
                    val = Bitmask.select(self.val, key.val)
                    vld = Bitmask.select(self.vldMask, key.val)
                return BitsVal(val, BIT, vld, updateTime=updateTime)
            elif key._dtype == SLICE:
                if keyVld:
                    firstBitNo = key.val[1].val
                    size = key._size()
                    val = Bitmask.selectRange(self.val, firstBitNo, size)
                    vld = Bitmask.selectRange(self.val, firstBitNo, size)
                retT = vecT(size, signed=self._dtype.signed)
                return BitsVal(val, retT, vld, updateTime=updateTime)
            else:
                raise NotImplementedError(key)
            
        elif isSlice or isSLICE:
            if isSlice:
                if key.step is not None:
                    raise NotImplementedError()
                start = key.start
                stop = key.stop
                
                if key.start is None:
                    start = boundryFromType(self, 0) + 1
                else:
                    start = toHVal(key.start)
                
                if key.stop is None:
                    stop = boundryFromType(self, 1)
                else:
                    stop = toHVal(key.stop)
            else:
                start = key.val[0]
                stop = key.val[1]

            isVal = iamVal and isinstance(start, Value) and isinstance(stop, Value) 
            if isVal:
                raise NotImplementedError("[TODO] bit select on value")
            else:
                key = (start - INT.fromPy(1))._downto(stop)
                resT = Bits(widthConstr=key, forceVector=True, signed=st.signed)
                
        elif isinstance(key, (int, IntegerVal)):
            key = toHVal(key)
            resT = BIT
            
        elif isinstance(key, RtlSignalBase):
            t = key._dtype
            if isinstance(t, Integer):
                resT = BIT
            elif isinstance(t, Slice):
                resT = Bits(widthConstr=key, forceVector=st.forceVector, signed=st.signed)
            elif isinstance(t, Bits):
                resT = BIT
                key = key._convert(INT)
            else:
                raise NotImplementedError("Index operation not implemented for index of type %s" % (repr(t)))
       
        else:
            raise NotImplementedError("Index operation not implemented for index %s" % (repr(key)))
            
        return Operator.withRes(AllOps.INDEX, [self, key], resT)

    def __setitem__(self, index, value):
        assert isinstance(self, Value)
        
        if index._isFullVld():
            if index._dtype == INT: 
                self.val = Bitmask.bitSetTo(self.val, index.val, value.val)
                self.vldMask = Bitmask.bitSetTo(self.vldMask, index.val, value.vldMask)
            elif index._dtype == SLICE:
                size = index._size()
                noOfFirstBit = index.val[1].val
                self.val = Bitmask.setBitRange(self.val, noOfFirstBit, size, value.val)
                self.vldMask = Bitmask.setBitRange(self.vldMask, noOfFirstBit, size, value.vldMask)
            else:
                raise NotImplementedError("Not implemented for index %s" % repr(index))
            self.updateTime = max(index.updateTime, value.updateTime)
        else:
            self.vldMask = 0

    def __invert__(self):
        if isinstance(self, Value):
            v = self.clone()
            v.val = ~v.val
            w = v._dtype.bit_length()
            v.val &= Bitmask.mask(w)
            return v
        else:
            try:
                # double negation
                d = self.singleDriver()
                if isinstance(d, Operator) and d.operator == AllOps.NOT:
                    return d.ops[0]
            except MultipleDriversExc:
                pass
            return Operator.withRes(AllOps.NOT, [self], self._dtype)
    
    # comparisons         
    def _eq(self, other):
        return bitsCmp(self, other, AllOps.EQ, lambda a, b : a == b)
    
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
       
    def __sub__(self, other):
        return bitsArithOp(self, other, AllOps.SUB)

    def __add__(self, other):
        return bitsArithOp(self, other, AllOps.ADD)
            
    
        
