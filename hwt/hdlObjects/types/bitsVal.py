from copy import copy
from operator import eq, ne, lt, gt, ge, le

from hwt.hdlObjects.operator import Operator
from hwt.hdlObjects.operatorDefs import AllOps
from hwt.hdlObjects.typeShortcuts import vecT
from hwt.hdlObjects.types.bitVal_bitOpsVldMask import vldMaskForXor, \
    vldMaskForAnd, vldMaskForOr
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.defs import BOOL, INT, BIT, SLICE
from hwt.hdlObjects.types.eventCapableVal import EventCapableVal
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.integerVal import IntegerVal
from hwt.hdlObjects.types.slice import Slice
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.hdlObjects.value import Value, areValues
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversExc
from hwt.hdlObjects.types.bitValFunctions import boundryFromType, \
    bitsCmp__val, bitsCmp, bitsBitOp__val, bitsBitOp, bitsArithOp__val, bitsArithOp, \
    getMulResT
from hwt.bitmask import mask, selectBit, selectBitRange, bitSetTo, \
    setBitRange

class BitsVal(EventCapableVal):
    """
    @attention: operator on signals are using value operator functions as well 
    """
    def _convSign__val(self, signed):
        if self._dtype.signed == signed:
            return self
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
    
    def _convSign(self, signed):
            if isinstance(self, Value):
                return self._convSign__val(signed)
            else:
                if self._dtype.signed == signed:
                    return self
                t = copy(self._dtype)
                t.signed = signed
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
        vld = 0 if val is None else mask(typeObj.bit_length())
        if not vld:
            val = 0
        return cls(int(val), typeObj, vld)
    
    def _concat__val(self, other):
        w = self._dtype.bit_length()
        other_w = other._dtype.bit_length()
        resWidth = w + other_w
        resT = vecT(resWidth)
        
        v = self.clone()
        v.val = (v.val << other_w) | other.val
        v.vldMask = (v.vldMask << other_w) | other.vldMask
        v.updateTime = max(self.updateTime, other.updateTime)
        v._dtype = resT
        
        return v 
    
    def _concat(self, other):
        w = self._dtype.bit_length()
        other_w = other._dtype.bit_length()
        resWidth = w + other_w
        resT = vecT(resWidth)
        
        if areValues(self, other):
            return self._concat__val(other)
        else:
            w = self._dtype.bit_length()
            other_w = other._dtype.bit_length()
            resWidth = w + other_w
            resT = vecT(resWidth)
            # is instance of signal
            if isinstance(other, InterfaceBase):
                other = other._sig
            if isinstance(other._dtype, Bits):
                if other._dtype.signed != None:
                    other = other._vec()
            elif other._dtype == BOOL:
                other = other._convert(BIT)
            else:
                raise TypeError(other._dtype)
            
            if self._dtype.signed != None:
                    self = self._vec()
            
            return Operator.withRes(AllOps.CONCAT, [self, other], resT)\
                           ._convert(vecT(resWidth, signed=self._dtype.signed))
    
    def _getitem__val(self, key):
        updateTime = max(self.updateTime, key.updateTime)
        keyVld = key._isFullVld() 
        val = 0
        vld = 0
        
        if isinstance(key._dtype, Integer):
            if keyVld:
                val = selectBit(self.val, key.val)
                vld = selectBit(self.vldMask, key.val)
            return BitsVal(val, BIT, vld, updateTime=updateTime)
        elif key._dtype == SLICE:
            if keyVld:
                firstBitNo = key.val[1].val
                size = key._size()
                val = selectBitRange(self.val, firstBitNo, size)
                vld = selectBitRange(self.vldMask, firstBitNo, size)
            retT = vecT(size, signed=self._dtype.signed)
            return BitsVal(val, retT, vld, updateTime=updateTime)
        else:
            raise TypeError(key)
    
    def __getitem__(self, key):
        iamVal = isinstance(self, Value)
        st = self._dtype
        l = st.bit_length()
        if l == 1:
            assert st.forceVector  # assert not indexing on single bit
            
        isSlice = isinstance(key, slice)
        isSLICE = isinstance(key, Slice.getValueCls())
        if areValues(self, key):
            return self._getitem__val(key)
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
                # [TODO] type can be wrong, but we need to get rid off widthConstr and use only width
                _resWidth = (start - 1 - stop)._downto(0)
                resT = Bits(widthConstr=_resWidth, forceVector=True, signed=st.signed)
                
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
                raise TypeError("Index operation not implemented for index of type %s" % (repr(t)))
       
        else:
            raise TypeError("Index operation not implemented for index %s" % (repr(key)))
            
        # [TODO] boundary check
        return Operator.withRes(AllOps.INDEX, [self, key], resT)

    def _setitem__val(self, index, value):
        if index._isFullVld():
            if isinstance(index._dtype, Integer): 
                self.val = bitSetTo(self.val, index.val, value.val)
                self.vldMask = bitSetTo(self.vldMask, index.val, value.vldMask)
            elif index._dtype == SLICE:
                size = index._size()
                noOfFirstBit = index.val[1].val
                self.val = setBitRange(self.val, noOfFirstBit, size, value.val)
                self.vldMask = setBitRange(self.vldMask, noOfFirstBit, size, value.vldMask)
            else:
                raise TypeError("Not implemented for index %s" % repr(index))
            self.updateTime = max(index.updateTime, value.updateTime)
        else:
            self.vldMask = 0

    def __setitem__(self, index, value):
        assert isinstance(self, Value)
        return self._setitem__val(index, value)

    def _invert__val(self):
        v = self.clone()
        v.val = ~v.val
        w = v._dtype.bit_length()
        v.val &= mask(w)
        return v
    
    def __invert__(self):
        if isinstance(self, Value):
            return self._invert__val()
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
    def _eq__val(self, other):
        return bitsCmp__val(self, other, AllOps.EQ, eq)
    def _eq(self, other):
        return bitsCmp(self, other, AllOps.EQ, eq)
    
    
    def _ne__val(self, other):
        return bitsCmp__val(self, other, AllOps.NEQ, ne)
    def __ne__(self, other):
        return bitsCmp(self, other, AllOps.NEQ)
    

    def _lt__val(self, other):
        return bitsCmp__val(self, other, AllOps.LOWERTHAN, lt)
    def __lt__(self, other):
        return bitsCmp(self, other, AllOps.LOWERTHAN)
    
    
    def _gt__val(self, other):
        return bitsCmp__val(self, other, AllOps.GREATERTHAN, gt)
    def __gt__(self, other):
        return bitsCmp(self, other, AllOps.GREATERTHAN)

    
    def _ge__val(self, other):
        return bitsCmp__val(self, other, AllOps.GE, ge)
    def __ge__(self, other):
        return bitsCmp(self, other, AllOps.GE)
   
   
    def _le__val(self, other):
        return bitsCmp__val(self, other, AllOps.LE, le)
    def __le__(self, other):
        return bitsCmp(self, other, AllOps.LE)
    
    
    def _xor__val(self, other):
        return bitsBitOp__val(self, other, AllOps.XOR, vldMaskForXor)
    def __xor__(self, other):
        return bitsBitOp(self, other, AllOps.XOR, vldMaskForXor)
    
    
    def _and__val(self, other):
        return bitsBitOp__val(self, other, AllOps.AND_LOG, vldMaskForAnd)
    def __and__(self, other):
        return bitsBitOp(self, other, AllOps.AND_LOG, vldMaskForAnd)
    
    
    def _or__val(self, other):
        return bitsBitOp__val(self, other, AllOps.OR_LOG, vldMaskForOr)
    def __or__(self, other):
        return bitsBitOp(self, other, AllOps.OR_LOG, vldMaskForOr)
       

    def _sub__val(self, other):
        return bitsArithOp__val(self, other, AllOps.SUB)
    def __sub__(self, other):
        return bitsArithOp(self, other, AllOps.SUB)
    
   
    def _add__val(self, other):
        return bitsArithOp__val(self, other, AllOps.ADD)
    def __add__(self, other):
        return bitsArithOp(self, other, AllOps.ADD)
    
    def _mul__val(self, other):
        resT = getMulResT(self._dtype, other._dtype)
        val = self.val * other.val
        result = resT.fromPy(val)
        
        raise NotImplementedError() 
        # # [TODO] value check range
        # if isinstance(other._dtype, Integer):
        #    if other.vldMask:
        #        v.vldMask = self.vldMask
        #    else:
        #        v.vldMask = 0
        #
        # elif isinstance(other._dtype, Bits):
        #    v.vldMask = self.vldMask & other.vldMask
        # else:
        #    raise TypeError("Incompatible type for multiplication: %s" % (repr(other._dtype)))
        # # [TODO] correct overflow detection for signed values
        # w = v._dtype.bit_length()
        # v.val &= Bitmask.mask(2*w)
        # v.updateTime = max(self.updateTime, other.updateTime)
        # return v
    def __mul__(self, other):        
        other = toHVal(other)
        assert isinstance(other._dtype, (Integer, Bits))
        
        
        if areValues(self, other):
            return self._mul__val(other)
        else:
            resT = getMulResT(self._dtype, other._dtype)
            if self._dtype.signed is None:
                self = self._unsigned()
            if isinstance(other._dtype, Bits) and other._dtype.signed is None:
                other = other._unsigned() 
            elif isinstance(other._dtype, Integer):
                pass
            else:
                raise TypeError("%s %s %s" % (repr(self), repr(AllOps.MUL) , repr(other)))
            
            subResT = vecT(resT.bit_length(), self._dtype.signed)
            o = Operator.withRes(AllOps.MUL, [self, other], subResT)
            return o._convert(resT)
        
