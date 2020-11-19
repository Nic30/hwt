from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, BOOL
from hwt.hdl.types.hdlType import default_auto_cast_fn, HdlType
from hwt.hdl.types.struct import HStruct
from hwt.hdl.types.union import HUnion
from hwt.hdl.value import HValue
from hwt.interfaces.structIntf import HdlTypeToIntf
from hwt.synthesizer.exceptions import TypeConversionErr
from hwt.synthesizer.hObjList import HObjList
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.vectorUtils import iterBits, fitTo_t
from pyMathBitPrecise.bit_utils import set_bit_range, mask


@internal
def convertBits__val(self: Bits, val: "BitVal", toType: HdlType):
    if toType == BOOL:
        return val != self.getValueCls().from_py(self, 0)
    elif isinstance(toType, Bits):
        if self.signed != toType.signed:
            if self.strict_sign and bool(self.signed) != bool(toType.signed):
                raise TypeConversionErr(self, toType)
            val = val._convSign__val(toType.signed)

        w_from, w_to = self.bit_length(), toType.bit_length()
        if w_from != w_to:
            if self.strict_width:
                raise TypeConversionErr(self, toType)
            if w_from > w_to:
                # cut off some bits from value
                new_m = val.vld_mask & toType.all_mask()
            else:
                # w_from < w_to, extend the value to some bit length
                extra_mask_bits = mask(w_to - w_from)
                new_m = set_bit_range(val.vld_mask, w_from, w_to - w_from, extra_mask_bits)
            val = toType.from_py(val.val, new_m)

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
def reinterpret_bits_to_hstruct__val(val, hStructT):
    """
    Reinterpret signal of type Bits to signal of type HStruct
    """
    container = hStructT.from_py(None)
    offset = 0
    for f in hStructT.fields:
        t = f.dtype
        width = t.bit_length()
        if f.name is not None:
            v = val[(width + offset):offset]
            v = v._reinterpret_cast(t)
            setattr(container, f.name, v)

        offset += width

    return container

@internal
def transfer_signals(src: InterfaceBase, dst: InterfaceBase):
    if src._interfaces:
        assert len(src._interfaces) == len(dst._interfaces), (src, dst)
        for si, di in zip(src._interfaces, dst._interfaces):
            transfer_signals(si, di)
    else:
        dst._sig = src._sig
        dst._sigInside = src._sigInside

            
@internal
def reinterpret_bits_to_hstruct(val, hStructT):
    """
    Reinterpret signal of type Bits to signal of type HStruct
    """
    container = HdlTypeToIntf(hStructT)
    container._loadDeclarations()
    offset = 0
    for f in hStructT.fields:
        t = f.dtype
        width = t.bit_length()
        if f.name is not None:
            v = val[(width + offset):offset]
            v = v._reinterpret_cast(t)
            current = getattr(container, f.name)
            if isinstance(v, InterfaceBase):
                transfer_signals(v, current)
            elif isinstance(v, HObjList):
                raise NotImplementedError()
            elif isinstance(v, (RtlSignal, HValue)):
                current._sig = v
            else:
                raise NotImplementedError()

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
        return reinterpret_bits_to_hstruct__val(val, toType)
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
