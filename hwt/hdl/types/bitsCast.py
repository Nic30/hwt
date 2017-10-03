from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.boolean import Boolean
from hwt.hdl.types.defs import INT
from hwt.hdl.types.hdlType import default_auto_cast_fn
from hwt.hdl.types.struct import HStruct
from hwt.hdl.types.union import HUnion
from hwt.hdl.value import Value
from hwt.synthesizer.vectorUtils import iterBits



def convertBits__val(self, val, toType):
    if isinstance(toType, Boolean):
        return val._eq(self.getValueCls().fromPy(1, self))
    elif isinstance(toType, Bits):
        return val._convSign__val(toType.signed)
    elif toType == INT:
        return INT.getValueCls()(val.val,
                                 INT,
                                 int(val._isFullVld()),
                                 val.updateTime)

    return default_auto_cast_fn(self, val, toType)


def convertBits(self, sigOrVal, toType):
    """
    Cast signed-unsigned, to int or bool 
    """
    if isinstance(sigOrVal, Value):
        return convertBits__val(self, sigOrVal, toType)
    elif isinstance(toType, Boolean):
        if self.bit_length() == 1:
            v = 0 if sigOrVal._dtype.negated else 1
            return sigOrVal._eq(self.getValueCls().fromPy(v, self))
    elif isinstance(toType, Bits):
        if self.bit_length() == toType.bit_length():
            return sigOrVal._convSign(toType.signed)
    elif toType == INT:
        return Operator.withRes(AllOps.BitsToInt, [sigOrVal], toType)

    return default_auto_cast_fn(self, sigOrVal, toType)



def bits_to_hstruct(sigOrVal, hStructT):
    """
    Reinterpret signal of type Bits to signal of type HStruct
    """
    container = hStructT.fromPy(None)
    offset = 0
    for f in hStructT.fields:
        t = f.dtype
        width = t.bit_length()
        if f.name is not None:
            s = sigOrVal[(width + offset):offset]
            s = s._reinterpret_cast(t)
            setattr(container, f.name, s)

        offset += width
        
    return container


def bits_to_harray(sigOrVal, hArrayT):
    elmT = hArrayT.elmType
    elmWidth = elmT.bit_length()
    a = hArrayT.fromPy(None)
    for i, item in enumerate(iterBits(sigOrVal, bitsInOne=elmWidth, skipPadding=False)):
        item = item._reinterpret_cast(elmT)
        a[i] = item

    return a


def reinterpretBits__val(self, val, toType):
    if isinstance(toType, HStruct):
        return bits_to_hstruct(val, toType)
    elif isinstance(toType, HUnion):
        raise NotImplementedError()
    elif isinstance(toType, HArray):
        return bits_to_harray(val, toType)
    else:
        return default_auto_cast_fn(self, val, toType)

def reinterpretBits(self, sigOrVal, toType):
    """
    Cast object of same bit size between to other type
    (f.e. bits to struct, union or array)
    """
    if isinstance(sigOrVal, Value):
        return reinterpretBits__val(self, sigOrVal, toType)
    elif self._dtype.bit_length() == toType.bit_length():
        if isinstance(toType, HStruct):
            raise bits_to_hstruct(sigOrVal, toType)
        elif isinstance(toType, HUnion):
            raise NotImplementedError()
        elif isinstance(toType, HArray):
            bits_to_harray(sigOrVal, toType)
    
    return default_auto_cast_fn(self, sigOrVal, toType)
