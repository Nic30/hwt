from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, BOOL
from hwt.hdl.types.hdlType import default_auto_cast_fn, HdlType
from hwt.hdl.types.struct import HStruct
from hwt.hdl.types.union import HUnion
from hwt.hdl.value import HValue
from hwt.synthesizer.vectorUtils import iterBits, fitTo_t
from hwt.synthesizer.exceptions import TypeConversionErr


@internal
def convertBits__val(self: Bits, val: "BitVal", toType: HdlType):
    if toType == BOOL:
        return val != self.getValueCls().from_py(self, 0)
    elif isinstance(toType, Bits):
        if self.signed != toType.signed:
            if self.strict_sign and bool(self.signed) != bool(toType.signed):
                raise TypeConversionErr(self, toType)
            val = val._convSign__val(toType.signed)

        if self.bit_length() != toType.bit_length():
            if self.strict_width:
                raise TypeConversionErr(self, toType)
            val = toType.from_py(val.val, val.vld_mask & toType.all_mask())
        if val._dtype != toType:
            # sign and width checked, only name, strict_* flags can be different
            val = toType.from_py(val.val, val.vld_mask)
        return val
    elif toType == INT:
        return INT.getValueCls()(INT, val.val,
                                 int(val._is_full_valid()))

    return default_auto_cast_fn(self, val, toType)


@internal
def convertBits(self: Bits, sigOrVal, toType: HdlType):
    """
    Cast Bit subtypes, (integers, bool, ...)
    """
    if isinstance(sigOrVal, HValue):
        return convertBits__val(self, sigOrVal, toType)
    elif toType == BOOL:
        if self.bit_length() == 1:
            v = 0 if sigOrVal._dtype.negated else 1
            return sigOrVal._eq(self.getValueCls().from_py(self, v))
    elif isinstance(toType, Bits):
        if self.bit_length() == toType.bit_length():
            if self.const is toType.const:
                return sigOrVal._convSign(toType.signed)

    return default_auto_cast_fn(self, sigOrVal, toType)


@internal
def reinterpret_bits_to_hstruct(sigOrVal, hStructT):
    """
    Reinterpret signal of type Bits to signal of type HStruct
    """
    container = hStructT.from_py(None)
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


@internal
def reinterpret_bits_to_harray(sigOrVal, hArrayT):
    elmT = hArrayT.element_t
    elmWidth = elmT.bit_length()
    a = hArrayT.from_py(None)
    for i, item in enumerate(iterBits(sigOrVal,
                                      bitsInOne=elmWidth,
                                      skipPadding=False)):
        item = item._reinterpret_cast(elmT)
        a[i] = item

    return a


@internal
def reinterpretBits__val(self: Bits, val, toType: HdlType):
    if isinstance(toType, Bits):
        if self.signed != toType.signed:
            val = val._convSign__val(toType.signed)
        return fitTo_t(val, toType)
    elif isinstance(toType, HStruct):
        return reinterpret_bits_to_hstruct(val, toType)
    elif isinstance(toType, HUnion):
        raise NotImplementedError()
    elif isinstance(toType, HArray):
        return reinterpret_bits_to_harray(val, toType)

    return default_auto_cast_fn(self, val, toType)


@internal
def reinterpretBits(self: Bits, sigOrVal, toType):
    """
    Cast object of same bit size between to other type
    (f.e. bits to struct, union or array)
    """
    if isinstance(sigOrVal, HValue):
        return reinterpretBits__val(self, sigOrVal, toType)
    elif isinstance(toType, Bits):
        if self.signed != toType.signed:
            sigOrVal = sigOrVal._convSign(toType.signed)
        return fitTo_t(sigOrVal, toType)
    elif sigOrVal._dtype.bit_length() == toType.bit_length():
        if isinstance(toType, HStruct):
            return reinterpret_bits_to_hstruct(sigOrVal, toType)
        elif isinstance(toType, HUnion):
            raise NotImplementedError()
        elif isinstance(toType, HArray):
            return reinterpret_bits_to_harray(sigOrVal, toType)

    return default_auto_cast_fn(self, sigOrVal, toType)
