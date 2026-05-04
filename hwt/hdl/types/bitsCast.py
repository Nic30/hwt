from typing import Union, Optional

from hwt.constants import NOT_SPECIFIED
from hwt.doc_markers import internal
from hwt.hObjList import HObjList
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsCastUtils import fitTo_t, BitWidthErr
from hwt.hdl.types.defs import INT
from hwt.hdl.types.hdlType import HdlType, default_auto_cast_fn, \
    default_explicit_cast_fn
from hwt.hdl.types.struct import HStruct
from hwt.hdl.types.union import HUnion
from hwt.hwIOs.hwIOArray import HwIOArray
from hwt.hwIOs.hwIOStruct import HdlType_to_HwIO
from hwt.mainBases import HwIOBase
from hwt.synthesizer.exceptions import TypeConversionErr
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.synthesizer.vectorUtils import iterBits
from pyMathBitPrecise.bit_utils import set_bit_range, mask


@internal
def HBits_auto_cast__HConst(curType: HBits, val: "HBitsConst", toType: HdlType):
    """
    :param curType: current type
    :param val: constant object to cast into toType
    :param toType: type to cast val to
    """
    if isinstance(toType, HBits):
        if toType == INT:
            return INT.getConstCls()(INT, val.val,
                                     int(val._is_full_valid()))
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

        if curType.is_bigendian != toType.is_bigendian:
            raise NotImplementedError(curType, '->', toType)

        if val._dtype != toType:
            # sign and width checked, only name, strict_* flags can be different
            val = toType._from_py(val.val, val.vld_mask)

        return val

    return default_auto_cast_fn(curType, val, toType)


@internal
def HBits_auto_cast__RtlSignal_try_reinterpret_flags(curType: HBits, v: Union[RtlSignal, HConst], toType: HdlType,
                                                     isConst: bool,
                                                     allowNegateCast: bool) -> Optional[Union[RtlSignal, HConst]]:
    # if curType.force_vector != toType.force_vector:
    #    raise NotImplementedError(curType, toType)
    if curType.const != toType.const:
        return None

    if curType.signed != toType.signed:
        if curType.strict_sign and bool(curType.signed) != bool(toType.signed):
            raise TypeConversionErr(curType, toType)
        v = v._cast_sign(toType.signed)
        curType = v._dtype

    if curType == toType:
        return v

    tWithSameFlagsAsDst = curType._createMutated(force_vector=toType.force_vector and toType.bit_length() == 1,
                                                 negated=toType.negated if allowNegateCast else NOT_SPECIFIED,
                                                 is_bigendian=toType.is_bigendian,
                                                 const=toType.const,
                                                 strict_sign=toType.strict_sign,
                                                 strict_width=toType.strict_width)
    if tWithSameFlagsAsDst == toType:
        if isConst:
            return toType._from_py(v.val, vld_mask=v.vld_mask)
        else:
            return HOperatorNode.withRes(HwtOps.BitsFlagCast, (v,), toType)


@internal
def HBits_auto_cast__RtlSignal(curType: HBits, sig: RtlSignal, toType: HdlType):
    """
    Cast Bit subtypes, (integers, bool, ...)
    """
    if isinstance(toType, HBits) and curType.bit_length() == toType.bit_length():
        if curType.bit_length() == 1:
            v = 0 if sig._dtype.negated else 1
            try:
                d = sig.singleDriver()
            except SignalDriverErr:
                d = None

            if d is not None and isinstance(d, HOperatorNode):
                if d.operator == HwtOps.BitsFlagCast and d.operands[0]._dtype == toType:
                    # xBool.cast(BIT).cast(BOOL) -> xBool
                    return d.operands[0]
                elif d.operator == HwtOps.NOT:
                    # signal itself is negated, ~a = 1 to a = 0
                    v = int(not bool(v))
                    sig = d.operands[0]

            c = curType.getConstCls().from_py(curType, v)
            return sig._eq(c)

        res = HBits_auto_cast__RtlSignal_try_reinterpret_flags(curType, sig, toType, False, False)
        if res is not None:
            return res

    return default_auto_cast_fn(curType, sig, toType)


@internal
def HBits_explicit_cast__RtlSignal(curType: HBits, v: RtlSignal, toType: HdlType):
    return HBits_explicit_cast__HConst(curType, v, toType, isHConst=False)


@internal
def HBits_explicit_cast__HConst(curType: HBits, v: RtlSignal, toType: HdlType, isHConst=True):
    if isinstance(toType, HBits):
        if curType.signed != toType.signed:
            v = v._cast_sign(toType.signed)
        v = fitTo_t(v, toType)
        if v._dtype == toType:
            return v
        else:
            return HBits_auto_cast__RtlSignal(v._dtype, v, toType)
        if curType.signed != toType.signed:
            v = v._cast_sign(toType.signed)
            curType = v._dtype
        res = HBits_auto_cast__RtlSignal_try_reinterpret_flags(curType, v, toType, isHConst, True)
        if res is not None:
            return res

    return default_explicit_cast_fn(curType, v, toType)


@internal
def HBits_reinterpret_cast_to_HStruct__HConst(val: HConst, hStructT: HStruct) -> HConst:
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

    if offset != val._dtype.bit_length():
        raise BitWidthErr("Src type contains more bits than dst", val._dtype.bit_length(), hStructT.bit_length(), val._dtype, hStructT)

    return container


@internal
def transfer_signals(src: Union[HwIOBase, HObjList], dst: Union[HwIOBase, HObjList]):
    if isinstance(src, HObjList):
        assert len(src) == len(dst)
        for si, di in zip(src, dst):
            transfer_signals(si, di)

    elif isinstance(src, (RtlSignal, HConst)):
        assert not dst._hwIOs, (src, dst)
        dst._sig = src

    elif src._hwIOs:
        # HwIOBase
        assert len(src._hwIOs) == len(dst._hwIOs), (src, dst)
        for si, di in zip(src._hwIOs, dst._hwIOs):
            transfer_signals(si, di)
    else:
        dst._sig = src._sig
        dst._sigInside = src._sigInside


@internal
def HBits_reinterpret_cast_to_HStruct__RtlSignal(val: RtlSignal, hStructT: HStruct):
    """
    Reinterpret signal of type :class:`HBits` to signal of type :class:`HStruct`
    """
    container = HdlType_to_HwIO().apply(hStructT)
    container._loadHwDeclarations()
    offset = 0
    for f in hStructT.fields:
        t = f.dtype
        width = t.bit_length()
        if f.name is not None:
            if offset == 0 and val._dtype.bit_length() == width:
                v = val
            else:
                v = val[(width + offset):offset]
            v = v._reinterpret_cast(t)
            current = getattr(container, f.name)
            transfer_signals(v, current)

        offset += width
    if offset != val._dtype.bit_length():
        raise BitWidthErr("Src type contains more bits than dst", val._dtype.bit_length(), hStructT.bit_length(), val._dtype, hStructT)

    return container


@internal
def HBits_reinterpret_cast_to_Harray(sigOrConst: Union[RtlSignal, HConst], hArrayT: HArray):
    elmT = hArrayT.element_t
    elmWidth = elmT.bit_length()
    if isinstance(sigOrConst, HConst):
        a = hArrayT.from_py(None)
        a.vld_mask = int(sigOrConst._is_full_valid())
    else:
        a = HwIOArray(None for _ in range(hArrayT.size))

    for i, item in enumerate(iterBits(sigOrConst,
                                      bitsInOne=elmWidth,
                                      skipPadding=False)):
        item = item._reinterpret_cast(elmT)
        a[i] = item

    return a


@internal
def HBits_reinterpret_cast__HConst(curType: HBits, v: HConst, toType: HdlType):
    if isinstance(toType, HBits):
        if curType.const == toType.const:
            if curType.bit_length() == toType.bit_length():
                return toType._from_py(v.val, v.vld_mask)
    elif isinstance(toType, HStruct):
        return HBits_reinterpret_cast_to_HStruct__HConst(v, toType)
    elif isinstance(toType, HUnion):
        raise NotImplementedError(curType, '->', toType)
    elif isinstance(toType, HArray):
        return HBits_reinterpret_cast_to_Harray(v, toType)

    return default_auto_cast_fn(curType, v, toType)


@internal
def HBits_reinterpret_cast__RtlSignal(curType: HBits, v: RtlSignal, toType: HdlType):
    """
    Cast object of same bit size between to other type
    (f.e. bits to struct, union or array)
    """
    if isinstance(toType, HBits):
        if curType.signed != toType.signed:
            v = v._cast_sign(toType.signed)
        if v._dtype == toType:
            return v
        res = HBits_auto_cast__RtlSignal_try_reinterpret_flags(curType, v, toType, False, True)
        if res is not None:
            return res
    elif v._dtype.bit_length() == toType.bit_length():
        if isinstance(toType, HStruct):
            return HBits_reinterpret_cast_to_HStruct__RtlSignal(v, toType)
        elif isinstance(toType, HUnion):
            raise NotImplementedError(curType, '->', toType)
        elif isinstance(toType, HArray):
            return HBits_reinterpret_cast_to_Harray(v, toType)

    return default_auto_cast_fn(curType, v, toType)
