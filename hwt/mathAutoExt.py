from operator import add, sub
from typing import Callable, Optional

from hwt.code import Concat
from hwt.doc_markers import hwt_expr_producer
from hwt.hdl.types.bitConstFunctions import AnyHBitsValue


@hwt_expr_producer
def extendForNoOverflowAddSub(a: AnyHBitsValue, b: AnyHBitsValue):
    """
    Increase bitwidth of two variables so overflow can not happen during add/sub
    """
    aSigned = bool(a._dtype.signed)
    bSigned = bool(b._dtype.signed)
    resWidth = max(a._dtype.bit_length(),
                   b._dtype.bit_length()) + \
               1 + (1 if aSigned != bSigned else 0)

    a = a._ext(resWidth)
    b = b._ext(resWidth)
    if aSigned != bSigned:
        if not aSigned:
            a = a._cast_sign(True)
        if not bSigned:
            b = b._cast_sign(True)

    return a, b


@hwt_expr_producer
def addAutoExt(a: AnyHBitsValue, b: AnyHBitsValue):
    a, b = extendForNoOverflowAddSub(a, b)
    return a + b


@hwt_expr_producer
def addAutoExtMany(*ops: tuple[AnyHBitsValue, ...]):
    a = ops[0]
    for b in ops[1:]:
        a, b = extendForNoOverflowAddSub(a, b)
        a = a + b
    return a


@hwt_expr_producer
def subAutoExt(a: AnyHBitsValue, b: AnyHBitsValue):
    a, b = extendForNoOverflowAddSub(a, b)
    return a - b


@hwt_expr_producer
def addShifted(a: AnyHBitsValue, b: AnyHBitsValue, bShift: int, maxResultWidth:Optional[int]=None,
               addSubFn:Callable[[AnyHBitsValue, AnyHBitsValue], AnyHBitsValue]=add) -> AnyHBitsValue:
    """
    perform a + (b<<shift) with a minimal or specified bitwidth without overflow
    """
    aIsSigned = bool(a._dtype.signed)
    bIsSigned = bool(b._dtype.signed)
    isSigned = aIsSigned or bIsSigned
    
    result: list[AnyHBitsValue] = []
    if maxResultWidth is not None:
        # assert maxResultWidth > bShift, ("sanity check that value is not fully shifted out", maxResultWidth, bShift)
        if maxResultWidth <= bShift:
            return a._extOrTrunc(maxResultWidth)._cast_sign(isSigned)

    if bShift > 0:
        widthL = a._dtype.bit_length()
        if bShift >= widthL:
            # b is shifted entirely before a
            result.append(a._ext(bShift))
            if maxResultWidth is not None:
                b = b._extOrTrunc(maxResultWidth - bShift)
            result.append(b)
            return Concat(*reversed(result))._cast_sign(isSigned)

        else:
            lowBits = a[bShift:]
            result.append(lowBits)
            a = a[:bShift]
    else:
        assert bShift == 0, bShift

    widthL = a._dtype.bit_length()
    widthR = b._dtype.bit_length()
    if maxResultWidth is not None:
        # trim a, b if it exceeds the result width (after offset is applied)
        w = maxResultWidth - bShift
        if widthL > w:
            a = a[w:]
            widthL = w
        if widthR > w:
            b = b[w:]
            widthR = w

    numWidth = max(widthL, widthR) + 1 + int(aIsSigned != bIsSigned)
    if maxResultWidth is not None:
        numWidth = min(numWidth, maxResultWidth - bShift)

    if widthL < numWidth:
        a = a._ext(numWidth)

    if widthR < numWidth:
        b = b._ext(numWidth)

    result.append(addSubFn(a._cast_sign(isSigned), b._cast_sign(isSigned)))

    res = Concat(*reversed(result))
    if maxResultWidth is not None:
        assert res._dtype.bit_length() <= maxResultWidth

    return res._cast_sign(isSigned)


@hwt_expr_producer
def subShifted(a: AnyHBitsValue, b: AnyHBitsValue, bShift: int, maxResultWidth:Optional[int]=None) -> AnyHBitsValue:
    return addShifted(a, b, bShift, maxResultWidth, sub)


@hwt_expr_producer
def addShiftedMany(ops:tuple[tuple[AnyHBitsValue, int]], maxResultWidth:Optional[int]=None,
                   addSubFn:Callable[[AnyHBitsValue, AnyHBitsValue], AnyHBitsValue]=add) -> AnyHBitsValue:
    a, sh = ops[0]
    assert sh == 0
    for b, bShift in ops[1:]:
        a = addShifted(a, b, bShift, maxResultWidth, addSubFn)
    return a

@hwt_expr_producer
def mulFullWidth(a: AnyHBitsValue, b: AnyHBitsValue) -> AnyHBitsValue:
    w = a._dtype.bit_length() + b._dtype.bit_length()
    return a._ext(w) * b._ext(w)
