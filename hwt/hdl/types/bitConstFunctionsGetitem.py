from typing import Union, Optional, Literal

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps, HOperatorDef
from hwt.hdl.types.bitConstFunctions import AnyHBitsValue, \
    HBitsAnyIndexCompatibleValue
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import INT, SLICE, BIT, BIT_N
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.sliceUtils import slice_to_HSlice
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import RtlSignalBase
from pyMathBitPrecise.bits3t import Bits3val


@internal
def _match_msb_get(v: "HBitsRtlSignal"):
    """
    :returns: x if v == x[x.width - 1] else None
    """
    if v._dtype.bit_length() != 1:
        return None

    opVIsResultOf = _get_operator_i_am_the_result_of(v)
    if opVIsResultOf == HwtOps.INDEX:
        iOp = v.singleDriver()
        iOpSrc, iOpI = iOp.operands
        if isinstance(iOpI, HConst) and iOpI._is_full_valid() and isinstance(iOpI._dtype, HBits) and int(iOpI) == iOpSrc._dtype.bit_length() - 1:
            return iOpSrc

    return None


@internal
def _fold_concat_of_msb_using_sext(v: "HBitsRtlSignal", vReplicatinCount:int, other: "HBitsRtlSignal", other_w: int):
    msbSrc = _match_msb_get(v)
    if msbSrc is other or other._dtype.bit_length() == 1 and v is other:
        # fold concat(x.msb, x) -> sext(x)
        return other._sext(other_w + vReplicatinCount)

    else:
        opOtherIsResultOf = _get_operator_i_am_the_result_of(other)
        if opOtherIsResultOf == HwtOps.SEXT and msbSrc == other.singleDriver().operands[0]:
            # fold concat(x.msb, sext(x)) -> sext(x)
            return msbSrc._sext(other_w + vReplicatinCount)
        elif opOtherIsResultOf == HwtOps.CONCAT:
            otherD: HOperatorNode = other.singleDriver()
            highBits, lowBits = otherD.operands
            if highBits is v:
                # fold concat(x1b, concat(x1b, y))) -> concat(sext(x1b), y)
                assert highBits._dtype.bit_length() == 1, highBits
                return highBits._sext(1 + vReplicatinCount)._concat(lowBits)
            elif highBits is msbSrc:
                # fold concat(x.msb, concat(x, y)) -> concat(sext(x), y)
                return highBits._sext(highBits._dtype.bit_length() + vReplicatinCount)._concat(lowBits)
            else:
                opHighBitsIsResultOf = _get_operator_i_am_the_result_of(highBits)
                if opHighBitsIsResultOf == HwtOps.SEXT:
                    hiBitsSrc = highBits.singleDriver().operands[0]
                    if hiBitsSrc is msbSrc:
                        # fold concat(x.msb, concat(sext(x), y)) -> concat(sext(x), y)
                        return msbSrc._sext(highBits._dtype.bit_length() + vReplicatinCount)._concat(lowBits)
    return None


@internal
def _get_operator_i_am_the_result_of(const_or_sig: Union[RtlSignalBase, HConst]) -> Optional[HOperatorDef]:
    if len(const_or_sig._rtlDrivers) == 1 and isinstance(const_or_sig._rtlObjectOrigin, HOperatorNode):
        return const_or_sig._rtlObjectOrigin.operator
    else:
        return None


@internal
def bitsGetitem_foldSliceOnCONCAT(v: AnyHBitsValue, start:int, stop: int, key: HBitsAnyIndexCompatibleValue) -> AnyHBitsValue:
    op_h, op_l = v._rtlObjectOrigin.operands
    op_l_w = op_l._dtype.bit_length()
    assert start > stop, (start, stop, "Should be in MSB:LSB format")
    if start <= op_l_w:
        # entirely in first operand of concat
        if op_l_w == 1:
            if isinstance(key._dtype, HSlice):
                assert int(key.val.start) == 1 and int(key.val.stop) == 0 and int(key.val.step) == -1, key
                return op_l
            else:
                assert int(key) == 0, key
                return op_l
        else:
            return op_l[key]
    elif stop >= op_l_w:
        # intirely in second operand of concat
        start -= op_l_w
        stop -= op_l_w
        if op_h._dtype.bit_length() == 1:
            assert start - stop == 1
            return op_h
        else:
            return op_h[SLICE.from_py(slice(start, stop, -1))]
    else:
        # partially in op_h and op_l, allpy slice on concat operands and return concatenation of it
        if stop != 0 or op_l._dtype.bit_length() > 1:
            op_l = op_l[:stop]

        if op_h._dtype.bit_length() == 1:
            assert start - op_l_w == 1, ("Out of range slice (but this error should be catched sooner)", v, key)
        else:
            op_h = op_h[start - op_l_w:0]

        return op_h._concat(op_l)


@internal
def bitsGetitem_foldSliceOnEXT(v: AnyHBitsValue,
                               start:int, stop: int,
                               key: HBitsAnyIndexCompatibleValue,
                               iAmResultOfOp: Literal[HwtOps.ZEXT, HwtOps.SEXT]) -> AnyHBitsValue:
    assert iAmResultOfOp in (HwtOps.ZEXT, HwtOps.SEXT), iAmResultOfOp
        # :note: start points at MSB and stop on LSB (start:stop, eg 8:0)
    extSrc = v.singleDriver().operands[0]
    extSrcWidth = extSrc._dtype.bit_length()
    resultWidth = start - stop
    if start < extSrcWidth:
        # selecting only bits from extSrc
        if stop == 0:
            return extSrc._trunc(start)
        else:
            return extSrc[key]

    elif stop >= extSrcWidth:
        # only msb bits are selected from ext and
        if iAmResultOfOp == HwtOps.ZEXT:
            return v._dtype._createMutated(resultWidth).from_py(0)
        else:
            return extSrc.getMsb()._sext(resultWidth)
    else:
        # selected value overlaps between extSrc and extension bits
        if stop != 0:
            extSrc = extSrc[:stop]
        return extSrc._ext(resultWidth, iAmResultOfOp == HwtOps.SEXT)


@internal
def bitsGetitem_foldBitGetOnEXT(v: AnyHBitsValue,
                                i:int,
                                key: HBitsAnyIndexCompatibleValue,
                                iAmResultOfOp: Literal[HwtOps.ZEXT, HwtOps.SEXT]) -> AnyHBitsValue:
    # fold zext(x)[i] -> x[i] if x.width < i else 0
    # fold sext(x)[i] -> x[i] if x.width < i else x.msb
    extSrc = v.singleDriver().operands[0]
    extSrcWidth = extSrc._dtype.bit_length()
    if i < extSrcWidth:
        # selecting only bits from extSrc
        return extSrc[key]
    else:
        # only msb bits are selected from ext and
        if iAmResultOfOp == HwtOps.ZEXT:
            return v._dtype._createMutated(1).from_py(0)
        else:
            return extSrc.getMsb()


@internal
def bitsGetitem_foldBitGetOnConcat(v: AnyHBitsValue, key: HBitsAnyIndexCompatibleValue, _index:int, iAmResultOfOp: Optional[HOperatorDef]):
    # index directly in the member of concatenation
    update_key = False
    while iAmResultOfOp == HwtOps.CONCAT:
        op_h, op_l = v._rtlObjectOrigin.operands
        op_l_w = op_l._dtype.bit_length()
        if _index < op_l_w:
            v = op_l
        else:
            v = op_h
            _index -= op_l_w
            update_key = True
        iamConst = isinstance(v, HConst)
        iAmResultOfOp = None if iamConst else _get_operator_i_am_the_result_of(v)
        # [todo] check if swap of negated flag can cause anything wrong

    if update_key:
        key = key._dtype.from_py(_index)

    return v, key


@internal
def bitsGetitem(v: AnyHBitsValue, iamConst:bool, key: HBitsAnyIndexCompatibleValue) -> AnyHBitsValue:
    """
    [] operator

    :attention: Table below is for little endian bit order (MSB:LSB)
        which is default.
        This is **reversed** as it is in pure python
        where it is [0, len(v)].

    :attention: Slice on slice signal is automatically reduced
        to single slice. This function also looks trough concatenations.

    +-----------------------------+----------------------------------------------------------------------------------+
    | a[up:low]                   | items low through up; a[16:8] selects upper byte from 16b vector a               |
    +-----------------------------+----------------------------------------------------------------------------------+
    | a[up:]                      | low is automatically substituted with 0; a[8:] will select lower 8 bits          |
    +-----------------------------+----------------------------------------------------------------------------------+
    | a[:end]                     | up is automatically substituted; a[:8] will select upper byte from 16b vector a  |
    +-----------------------------+----------------------------------------------------------------------------------+
    | a[:], a[-1], a[-2:], a[:-2] | raises NotImplementedError   (not implemented due to complicated support in hdl) |
    +-----------+----------------------------------------------------------------------------------------------------+

    :note: signed is preserved as in VHDL, and not like in Verilog where result of slice is always unsigned
    """
    st = v._dtype
    vWidth = st.bit_length()

    if isinstance(key, slice):
        key = slice_to_HSlice(key, vWidth)
        isSLICE = True
    else:
        isSLICE = isinstance(key, HSlice.getConstCls())

    is1bScalar = vWidth == 1 and not st.force_vector
    if not isSLICE:
        if is1bScalar and \
                ((isinstance(key, int) and key == 0) or\
                 (isinstance(key, HConst) and key._is_full_valid() and int(key) == 0)):
            return v
        key = toHVal(key, INT)
    else:
        if is1bScalar and key.val.start == 1 and key.val.stop == 0 and key.val.step == -1:
            return v

    if is1bScalar:
        # assert not indexing on single bit
        raise IndexError("indexing on single bit")

    iAmResultOfOp = None if iamConst else _get_operator_i_am_the_result_of(v)
    if iAmResultOfOp == HwtOps.TRUNC:
        # fold trunc(x)[i] to x[i]
        return v.singleDriver().operands[0][key]

    HBits = v._dtype.__class__
    if isSLICE:
        # :note: downto notation
        start = key.val.start
        stop = key.val.stop
        if key.val.step != -1:
            raise NotImplementedError()

        startIsConst = isinstance(start, HConst)
        stopIsConst = isinstance(stop, HConst)
        indexesAreHConst = startIsConst and stopIsConst
        if indexesAreHConst and start.val == vWidth and stop.val == 0:
            # selecting all bits no conversion needed
            # fold x[h:l] -> x
            return v

        # check start boundaries
        if startIsConst:
            _start = int(start)
            if _start < 0 or _start > vWidth:
                raise IndexError("start index is out of range start:", _start, " width:", vWidth, "")

        # check end boundaries
        if stopIsConst:
            _stop = int(stop)
            if _stop < 0 or _stop >= vWidth:
                raise IndexError("stop index is out of range stop:", _stop, " width:", vWidth)

        # check width of selected range
        if startIsConst and stopIsConst and _start - _stop <= 0:
            raise IndexError("start (represents MSB bit index +1) must be > stop (represents LSB bit index)", _start, _stop)

        if iAmResultOfOp == HwtOps.INDEX:
            # try reduce v and parent slice to one
            # fold x[a:b][start:stop] -> x[b+start:b+stop]
            original, parentIndex = v._rtlObjectOrigin.operands
            if isinstance(parentIndex._dtype, HSlice):
                parentLower = parentIndex.val.stop
                start = parentLower + start
                stop = parentLower + stop
                return original[start:stop]

        elif startIsConst and stopIsConst:
            # index directly in the member of concatenation
            # :note: start points at MSB and stop on LSB (start:stop, eg 8:0)
            stop = int(stop)
            start = int(start)
            if iAmResultOfOp == HwtOps.CONCAT:
                return bitsGetitem_foldSliceOnCONCAT(v, start, stop, key)
            elif iAmResultOfOp == HwtOps.ZEXT or iAmResultOfOp == HwtOps.SEXT:
                return bitsGetitem_foldSliceOnEXT(v, start, stop, key, iAmResultOfOp)
            elif stop == 0:
                return v._trunc(start)

        if iamConst:
            if isinstance(key, SLICE.getConstCls()):
                key = key.val
            res = Bits3val.__getitem__(v, key)
            if res._dtype.bit_length() == 1 and not res._dtype.force_vector:
                assert res._dtype is not v._dtype
                res._dtype.force_vector = True
            return res
        else:
            key = SLICE.from_py(slice(start, stop, -1))
            _resWidth = start - stop
            resT = HBits(bit_length=_resWidth, force_vector=_resWidth == 1,
                        signed=st.signed, negated=st.negated)

    elif isinstance(key, HBits.getConstCls()):
        # int like value addressing a single bit
        if st.negated:
            resT = BIT_N
        else:
            resT = BIT
        if not key._is_full_valid():
            return resT.from_py(None)

        # check index range
        _index = int(key)
        if _index < 0 or _index > vWidth - 1:
            raise IndexError(_index)

        if iAmResultOfOp == HwtOps.INDEX:
            # index directly in parent signal
            # fold x[a:b][i] -> x[b+i]
            original, parentIndex = v._rtlObjectOrigin.operands
            if isinstance(parentIndex._dtype, HSlice):
                parentLower = parentIndex.val.stop
                return original[parentLower + _index]

        elif iAmResultOfOp == HwtOps.TRUNC:
            # fold x._trunc(n)[i] to x[i]
            original = v._rtlObjectOrigin.operands[0]
            return original[_index]

        elif iAmResultOfOp == HwtOps.ZEXT or iAmResultOfOp == HwtOps.SEXT:
            return bitsGetitem_foldBitGetOnEXT(v, _index, key, iAmResultOfOp)

        else:
            # index directly in the member of concatenation
            # fold concat(a, x)[i] -> x[i]
            v, key = bitsGetitem_foldBitGetOnConcat(v, key, _index, iAmResultOfOp)
            st = v._dtype
            if isinstance(key, HBits.getConstCls()) and int(key) == 0 and (
                    v._dtype.bit_length() == 1 and not v._dtype.force_vector
                ):
                return v

        if iamConst:
            # at the end because multiple non-constant indexes may be applied on constant and we want to merge them
            return Bits3val.__getitem__(v, key)
        elif key._is_full_valid() and int(key) == 0 and v._dtype == BIT or v._dtype == BIT_N:
            return v

    elif isinstance(key, RtlSignalBase):
        t = key._dtype
        if isinstance(t, HSlice):
            bit_length = key.staticEval()._size()
            resT = HBits(bit_length,
                        force_vector=bit_length == 1,
                        signed=st.signed,
                        negated=st.negated)
        elif isinstance(t, HBits):
            resT = BIT
        else:
            raise TypeError(
                "Index operation not implemented"
                " for index of type ", t)

    else:
        raise TypeError(
            "Index operation not implemented for index ", key)

    if st.negated and resT is BIT:
        resT = BIT_N

    return HOperatorNode.withRes(HwtOps.INDEX, [v, key], resT)

