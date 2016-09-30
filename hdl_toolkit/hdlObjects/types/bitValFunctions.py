from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.value import Value, areValues
from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.typeShortcuts import vecT
from hdl_toolkit.bitmask import mask

BoolVal = BOOL.getValueCls()

def bitsCmp__val(self, other, op, evalFn):
    w = self._dtype.bit_length()
    assert w == other._dtype.bit_length(), "%d, %d" % (w, other._dtype.bit_length())
    
    vld = self.vldMask & other.vldMask
    _vld = vld == mask(w)
    res = evalFn(self.val, other.val) and _vld
    updateTime = max(self.updateTime, other.updateTime)
    
    return BoolVal(res, BOOL, int(_vld), updateTime)

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
        return bitsCmp__val(self, other, op, evalFn)
    else:
        if other._dtype == BOOL:
            self = self._convert(BOOL)
        elif self._dtype == other._dtype:
            pass
        elif isinstance(other._dtype, Integer):
            other = other._convert(self._dtype) 
        else:
            raise TypeError("Types are not comparable (%s, %s)" % (repr(self._dtype), repr(other._dtype)))
        
        return Operator.withRes(op, [self, other], BOOL) 

def bitsBitOp__val(self, other, op, getVldFn):
    w = self._dtype.bit_length()
    assert w == other._dtype.bit_length()
    
    vld = getVldFn(self, other)
    res = op._evalFn(self.val, other.val) & vld
    updateTime = max(self.updateTime, other.updateTime)
    
    return self.__class__(res, self._dtype, vld, updateTime)

def bitsBitOp(self, other, op, getVldFn):
    """
    @attention: If other is Bool signal, convert this to boolean (not ideal, due VHDL event operator)
    """
    other = toHVal(other)
    
    iamVal = isinstance(self, Value)
    otherIsVal = isinstance(other, Value) 
    
    if iamVal and otherIsVal:
        return bitsBitOp__val(self, other, op, getVldFn)
    else:
        if other._dtype == BOOL:
            self = self._convert(BOOL)
        elif self._dtype == other._dtype:
            pass
        else:
            raise TypeError("Types are not comparable (%s, %s)" % 
                                       (repr(self._dtype), repr(other._dtype)))
        
        return Operator.withRes(op, [self, other], self._dtype) 

def bitsArithOp__val(self, other, op):
    v = self.clone()
    v.val = op._evalFn(self.val, other.val)

    # [TODO] correct overflow detection for signed values
    w = v._dtype.bit_length()
    v.val &= mask(w)
    
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

def bitsArithOp(self, other, op):
    other = toHVal(other)
    assert isinstance(other._dtype, (Integer, Bits))
    if areValues(self, other):
        return bitsArithOp__val(self, other, op)
    else:
        resT = self._dtype
        if self._dtype.signed is None:
            self = self._unsigned()
        if isinstance(other._dtype, Bits) and other._dtype.signed is None:
            other = other._unsigned() 
        elif isinstance(other._dtype, Integer):
            pass
        else:
            raise TypeError("%s %s %s" % (repr(self), repr(op) , repr(other)))
        
        o = Operator.withRes(op, [self, other], self._dtype)
        return o._convert(resT)

def boundryFromType(sigOrVal, boundaryIndex):
    c = sigOrVal._dtype.constrain
    if isinstance(c, Value):  # slice
        return c.val[boundaryIndex]
    else:  # downto / to
        return c.singleDriver().ops[boundaryIndex]

def getMulResT(firstT, secondT):
    if isinstance(secondT, Integer):
        raise NotImplementedError()
    
    width = firstT.bit_length() + secondT.bit_length()
    return vecT(width, firstT.signed)
    
