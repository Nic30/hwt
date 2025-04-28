from typing import Union

from hwt.doc_markers import internal
from hwt.hObjList import HObjList
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsCastUtils import fitTo_t
from hwt.hdl.types.defs import INT, BOOL
from hwt.hdl.types.hdlType import HdlType, default_auto_cast_fn
from hwt.hdl.types.struct import HStruct
from hwt.hdl.types.union import HUnion
from hwt.hwIOs.hwIOStruct import HdlType_to_HwIO
from hwt.mainBases import HwIOBase
from hwt.synthesizer.exceptions import TypeConversionErr
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.vectorUtils import iterBits
from pyMathBitPrecise.bit_utils import set_bit_range, mask


@internal
def convertBits__HConst(curType: HBits, val: "HBitsConst", toType: HdlType):
    """
    :param curType: current type
    :param val: constant object to cast into toType
    :param toType: type to cast val to
    """
    if toType == BOOL:
        return val != curType.getConstCls().from_py(curType, 0)
    elif isinstance(toType, HBits):
        if curType.signed != toType.signed:
            if curType.strict_sign and bool(curType.signed) != bool(toType.signed):
                raise TypeConversionErr(curType, toType)
            val = val._cast_sign(toType.signed)

        w_from, w_to = curType.bit_length(), toType.bit_length()
        if w_from != w_to:
            if curType.strict_width:
                raise TypeConversionErr(curType, toType)
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
        return INT.getConstCls()(INT, val.val,
                                 int(val._is_full_valid()))

    return default_auto_cast_fn(curType, val, toType)


@internal
def convertBits__RtlSignal(curType: HBits, sig: RtlSignal, toType: HdlType):
    """
    Cast Bit subtypes, (integers, bool, ...)
    """
    if toType == BOOL:
        if curType.bit_length() == 1:
            v = 0 if sig._dtype.negated else 1
            if isinstance(sig, RtlSignal):
                sig: RtlSignal
                try:
                    d = sig.singleDriver()
                except SignalDriverErr:
                    d = None

                if d is not None and isinstance(d, HOperatorNode) and d.operator == HwtOps.NOT:
                    # signal itself is negated, ~a = 1 to a = 0
                    v = int(not bool(v))
                    sig = d.operands[0]

            return sig._eq(curType.getConstCls().from_py(curType, v))
    elif isinstance(toType, HBits):
        if curType.bit_length() == toType.bit_length():
            # if curType.force_vector != toType.force_vector:
            #    raise NotImplementedError(curType, toType)

            if curType.const == toType.const:
                return sig._cast_sign(toType.signed)

    return default_auto_cast_fn(curType, sig, toType)


@internal
def reinterpret_bits_to_hstruct__HConst(val: HConst, hStructT: HStruct):
    """
    Reinterpret signal of type HBits to signal of type HStruct
    """
    container = hStructT.from_py(None)
    hStructT.vld_mask = int(val._is_full_valid())
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
def transfer_signals(src: HwIOBase, dst: HwIOBase):
    if src._hwIOs:
        assert len(src._hwIOs) == len(dst._hwIOs), (src, dst)
        for si, di in zip(src._hwIOs, dst._hwIOs):
            transfer_signals(si, di)
    else:
        dst._sig = src._sig
        dst._sigInside = src._sigInside


@internal
def reinterpret_bits_to_hstruct__RtlSignal(val: RtlSignal, hStructT: HStruct):
    """
    Reinterpret signal of type HBits to signal of type HStruct
    """
    container = HdlType_to_HwIO().apply(hStructT)
    container._loadHwDeclarations()
    offset = 0
    for f in hStructT.fields:
        t = f.dtype
        width = t.bit_length()
        if f.name is not None:
            v = val[(width + offset):offset]
            v = v._reinterpret_cast(t)
            current = getattr(container, f.name)
            if isinstance(v, HwIOBase):
                transfer_signals(v, current)
            elif isinstance(v, HObjList):
                raise NotImplementedError()
            elif isinstance(v, (RtlSignal, HConst)):
                current._sig = v
            else:
                raise NotImplementedError()

        offset += width

    return container


@internal
def reinterpret_bits_to_harray(sigOrConst: Union[RtlSignal, HConst], hArrayT: HArray):
    elmT = hArrayT.element_t
    elmWidth = elmT.bit_length()
    if isinstance(sigOrConst, HConst):
        a = hArrayT.from_py(None)
        a.vld_mask = int(sigOrConst._is_full_valid())
    else:
        a = HObjList([None for _ in range(hArrayT.size)])

    for i, item in enumerate(iterBits(sigOrConst,
                                      bitsInOne=elmWidth,
                                      skipPadding=False)):
        item = item._reinterpret_cast(elmT)
        a[i] = item

    return a


@internal
def reinterpretBits__HConst(curType: HBits, val: HConst, toType: HdlType):
    if isinstance(toType, HBits):
        if curType.signed != toType.signed:
            val = val._cast_sign(toType.signed)
        return fitTo_t(val, toType)
    elif isinstance(toType, HStruct):
        return reinterpret_bits_to_hstruct__HConst(val, toType)
    elif isinstance(toType, HUnion):
        raise NotImplementedError()
    elif isinstance(toType, HArray):
        return reinterpret_bits_to_harray(val, toType)

    return default_auto_cast_fn(curType, val, toType)


@internal
def reinterpretBits__RtlSignal(curType: HBits, sig: RtlSignal, toType: HdlType):
    """
    Cast object of same bit size between to other type
    (f.e. bits to struct, union or array)
    """
    if isinstance(toType, HBits):
        if curType.signed != toType.signed:
            sig = sig._cast_sign(toType.signed)
        return fitTo_t(sig, toType)
    elif sig._dtype.bit_length() == toType.bit_length():
        if isinstance(toType, HStruct):
            return reinterpret_bits_to_hstruct__RtlSignal(sig, toType)
        elif isinstance(toType, HUnion):
            raise NotImplementedError()
        elif isinstance(toType, HArray):
            return reinterpret_bits_to_harray(sig, toType)

    return default_auto_cast_fn(curType, sig, toType)
