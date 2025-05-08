from typing import Union, Optional

from hdlConvertorAst.hdlAst import HdlValueInt
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOp, HdlOpType, \
    HDLCONVERTAST_OPS_SHIFT_AND_ROT, HdlOthers
from hdlConvertorAst.hdlAst._statements import HdlStmAssign
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call, \
    hdl_index, hdl_downto
from hwt.code import If
from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps, CAST_OPS
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.utils.listOfHdlStatements import ListOfHdlStatement
from hwt.hdl.types.bitConstFunctions import AnyHBitsValue
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsConst import HBitsConst
from hwt.hdl.types.bitsRtlSignal import HBitsRtlSignal
from hwt.hdl.types.defs import BOOL, INT, BIT
from hwt.mainBases import RtlSignalBase
from hwt.serializer.hwt.ops import ToHdlAstHwt_ops
from hwt.serializer.vhdl.types import ToHdlAstVhdl2008_types
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from pyMathBitPrecise.bit_utils import mask


@internal
def isResultOfTypeConversionForIndex(sig: RtlSignal):
    if len(sig._rtlDrivers) != 1:
        return False

    if sig._isUnnamedExpr:
        d = sig.singleDriver()
        return d.operator not in (HwtOps.INDEX, HwtOps.TRUNC)

    return False


def matchZextOrSextArg(op: Union[RtlSignal, HConst], srcWidth:int) -> tuple[Optional[AnyHBitsValue], Optional[bool]]:
    """
    Check if the value is zext or sext to double width
    :returns: base operand, isSigned or None, None if not matched
    """
    if isinstance(op, HConst):
        prefixBits = op.val >> srcWidth
        if prefixBits == 0:
            return op[srcWidth:], False
        elif prefixBits == mask(srcWidth):
            return op[srcWidth:], True

    elif op._isUnnamedExpr:
        try:
            d = op.singleDriver()
        except SignalDriverErr:
            return None, None
        casts = []
        # drop unnecessary casts
        while isinstance(d, HOperatorNode) and d.operator in CAST_OPS:
            casts.append(d.operator)
            d = d.operands[0].singleDriver()

        if isinstance(d, HOperatorNode) and d.operator in (HwtOps.ZEXT, HwtOps.SEXT):
            src = d.operands[0]
            if src._dtype.bit_length() == srcWidth:
                return src, d.operator == HwtOps.SEXT

    return None, None


def matchFullWidthMul(op0: Union[RtlSignal, HConst], op1: Union[RtlSignal, HConst])\
     ->tuple[bool, bool, Union[RtlSignal, HConst], Union[RtlSignal, HConst]]:
        # result of multiplication in VHDL has 2x width, while in hwt has same width as operands have
    # truncatenation is required,
    # * first we check if operands are not zero extended to double width
    #   if this is the case we can use original operands and avoid any cast
    sextMulMatch = False
    zextMulMatch = False
    width = op0._dtype.bit_length() // 2
    _op0, _op0SignExtended = matchZextOrSextArg(op0, width)
    if _op0 is not None:
        _op1, _op1SignExtended = matchZextOrSextArg(op1, width)
        if _op1 is not None:
            if _op0SignExtended == _op1SignExtended:
                op0 = _op0._cast_sign(_op0SignExtended)
                op1 = _op1._cast_sign(_op1SignExtended)
                if _op0SignExtended:
                    sextMulMatch = True
                else:
                    zextMulMatch = True

    # * else we need to truncatenate result to width of operand
    return zextMulMatch, sextMulMatch, op0, op1


class ToHdlAstVhdl2008_ops(ToHdlAstVhdl2008_types):
    op_transl_dict = {
        **ToHdlAstHwt_ops.op_transl_dict,
        HwtOps.RISING_EDGE: HdlOpType.RISING,
        HwtOps.FALLING_EDGE: HdlOpType.FALLING,
    }

    TO_INTEGER = HdlValueId("TO_INTEGER", obj=LanguageKeyword())
    _cast_ops = {
        HwtOps.BitsAsSigned: ToHdlAstVhdl2008_types.SIGNED,
        HwtOps.BitsAsUnsigned: ToHdlAstVhdl2008_types.UNSIGNED,
        HwtOps.BitsAsVec: ToHdlAstVhdl2008_types.STD_LOGIC_VECTOR,
    }

    RESIZE = HdlValueId("RESIZE", obj=LanguageKeyword())
    SHIFT_LEFT = HdlValueId("SHIFT_LEFT", obj=LanguageKeyword())
    SHIFT_RIGHT = HdlValueId("SHIFT_RIGHT", obj=LanguageKeyword())
    ROTATE_LEFT = HdlValueId("ROTATE_LEFT", obj=LanguageKeyword())
    ROTATE_RIGHT = HdlValueId("ROTATE_RIGHT", obj=LanguageKeyword())
    # :note: bool in HDLCONVERTORAST_TO_VHDL value marks if shift is arithmetical or logical
    HDLCONVERTORAST_TO_VHDL = {
        HdlOpType.SLL: (SHIFT_LEFT, False),  # shift left logical
        HdlOpType.SRL: (SHIFT_RIGHT, False),  # shift right logical
        HdlOpType.SLA: (SHIFT_LEFT, True),  # shift left arithmetical
        HdlOpType.SRA: (SHIFT_RIGHT, True),  # shift right arithmetical
        HdlOpType.ROL: (ROTATE_LEFT, False),  # rotate left
        HdlOpType.ROR: (ROTATE_RIGHT, False),  # rotate right

    }

    @internal
    def _tmp_var_for_ternary(self, val: RtlSignal) -> RtlSignal:
        """
        Optionally convert boolean to std_logic_vector
        """
        isNew, o = self.tmpVars.create_var_cached(
            "tmpTernary_",
            val._dtype,
            postponed_init=True,
            extra_args=(val, bool, 1, 0))
        if isNew:
            cond, ifTrue, ifFalse = val._rtlDrivers[0].operands
            if_ = If(cond)
            if_.ifTrue.append(HdlAssignmentContainer(ifTrue, o,
                                         virtual_only=True,
                                         parentStm=if_))
            if_.ifFalse = ListOfHdlStatement()
            if_.ifFalse.append(HdlAssignmentContainer(ifFalse, o,
                                          virtual_only=True,
                                          parentStm=if_))
            if_._outputs.append(o)
            for obj in (cond, ifTrue, ifFalse):
                if isinstance(obj, RtlSignalBase):
                    if_._inputs.append(obj)
            o._rtlDrivers.append(if_)
            if_._discover_enclosure()
            self.tmpVars.finish_var_init(o)

        return o

    @internal
    def _tmp_var_for_arrayAggregate(self, val: RtlSignal) -> RtlSignal:
        """
        Create tmp variable for expression which will be converted to VHDL aggreate expression:
        .. code-block::
           x = x1b._sext(10)
           xTmp10b := (0=> x1b, others=>x1b);
            
        """
        _, o = self.tmpVars.create_var_cached(
            "tmpAggregate_",
            val._dtype,
            def_val=val,
            extra_args=(val, HdlOpType.MAP_ASSOCIATION))
        return o

    def _as_Bits(self, val: Union[RtlSignal, HConst]):
        if val._dtype == BOOL:
            bit1_t = HBits(1)
            isNew, o = self.tmpVars.create_var_cached(
                "tmpBool2std_logic_",
                bit1_t,
                postponed_init=True,
                extra_args=(val, int, 1, 0))
            if isNew:
                ifTrue, ifFalse = bit1_t.from_py(1), bit1_t.from_py(0)
                if_ = If(val)
                if_.ifTrue.append(HdlAssignmentContainer(ifTrue, o, virtual_only=True, parentStm=if_))
                if_.ifFalse = []
                if_.ifFalse.append(HdlAssignmentContainer(ifFalse, o, virtual_only=True, parentStm=if_))
                if_._outputs.append(o)
                o._rtlDrivers.append(if_)
                self.tmpVars.finish_var_init(o)
            return o
        else:
            assert isinstance(val._dtype, HBits), val._dtype
            return val

    def _as_Bits_vec(self, val: Union[RtlSignal, HConst]):
        val = self._as_Bits(val)
        t = val._dtype
        if not t.force_vector and t.bit_length() == 1:
            # std_logic -> std_logic_vector
            std_logic_vector = HBits(1, signed=t.signed, force_vector=True)
            isNew, o = self.tmpVars.create_var_cached(
                "tmp_std_logic2vector_",
                std_logic_vector,
                postponed_init=True,
                extra_args=(val, std_logic_vector))
            if isNew:
                o._rtlDrivers.append(HdlAssignmentContainer(val, o, virtual_only=True))
                self.tmpVars.finish_var_init(o)
            return o
        else:
            # already a std_logic_vector
            return val

    def as_hdl_operand(self, operand: Union[RtlSignal, HConst]):
        # automatically extract some operators as tmp variable
        # * nested ternary in expressions like
        #   ( '1'  WHEN r = f ELSE  '0' ) & "0"
        # * nested array aggregate expressions
        #   (0=>x, 1=>y) & "0"
        isTernaryOp = False
        isArrayAggregateOp = False
        try:
            if operand._isUnnamedExpr:
                d = operand._rtlDrivers[0]
                o = d.operator
                if o == HwtOps.TERNARY:
                    isTernaryOp = True
                elif o == HwtOps.SEXT or o == HwtOps.ZEXT:
                    op0T = d.operands[0]._dtype
                    if op0T.signed is None and op0T.bit_length() == 1 and not op0T.force_vector:
                        isArrayAggregateOp = True

        except (AttributeError, IndexError):
            pass

        if isTernaryOp:
            # rewrite ternary operator as if
            operand = self._tmp_var_for_ternary(operand)
        elif isArrayAggregateOp:
            operand = self._tmp_var_for_arrayAggregate(operand)

        return self.as_hdl(operand)

    def apply_cast(self, t: HdlValueId, op):
        return hdl_call(t, [op, ])

    def _wrapConcatInTmpVariable(self, op):
        if isinstance(op, RtlSignalBase) and op._isUnnamedExpr:
            # if left operand is concatenation and this is not concatenation we must extract it as tmp variable
            # because VHDL would not be able to resolve type of concatenated signal otherwise
            try:
                d = op.singleDriver()
            except SignalDriverErr:
                d = None

            if d is not None and isinstance(d, HOperatorNode) and d.operator is HwtOps.CONCAT:
                _, op = self.tmpVars.create_var_cached("tmpConcatExpr_", op._dtype, def_val=op)
        return op

    def _as_hdl_HOperatorNode_mulWithTrunc(self, op: HOperatorNode, srcOperandType: HBits, _op0, _op1):
        # new tmp variable must be created because downto may be applied only on ID and not expression
        width = srcOperandType.bit_length()
        isNew, tmpMulTruncVar = self.tmpVars.create_var_cached(
            "tmpMulTrunc_",
            HBits(width * 2, srcOperandType.signed),
            postponed_init=True,
            extra_args=(op,))
        if isNew:
            hdl = self.tmpVars.extraVarsHdl
            hdl_a = HdlStmAssign(HdlOp(HdlOpType.MUL, [_op0, _op1]), self.as_hdl_HdlSignalItem(tmpMulTruncVar))
            hdl_a.is_blocking = True
            hdl.append(hdl_a)
            as_hdl = self.as_hdl_HdlSignalItem(tmpMulTruncVar, declaration=True)
            hdl.append(as_hdl)

        return hdl_index(self.as_hdl_HdlSignalItem(tmpMulTruncVar),
                         hdl_downto(self.as_hdl_int(width - 1), self.as_hdl_int(0)))

    def as_hdl_HOperatorNode_indexRhs(self, op1: Union[HBitsConst, HBitsRtlSignal]):
        if isinstance(op1._dtype, HBits) and op1._dtype != INT:
            if op1._dtype.signed is None:
                if op1._dtype.bit_length() == 1 and not op1._dtype.force_vector:
                    _, op1 = self.tmpVars.create_var_cached("tmp1bToUnsigned_", HBits(1, force_vector=True), def_val=op1)
                _op1 = self.as_hdl_operand(op1)
                _op1 = self.apply_cast(self.UNSIGNED, _op1)
            else:
                _op1 = self.as_hdl_operand(op1)

            return self.apply_cast(self.TO_INTEGER, _op1)
        else:
            return self.as_hdl_operand(op1)

    def as_hdl_HOperatorNode(self, op: HOperatorNode):
        ops = op.operands
        o = op.operator

        if o == HwtOps.INDEX:
            op0, op1 = ops
            if isinstance(op0, RtlSignalBase) and isResultOfTypeConversionForIndex(op0):
                _, op0 = self.tmpVars.create_var_cached("tmpTypeConv_", op0._dtype, def_val=op0)
            if isinstance(op1, RtlSignalBase) and isResultOfTypeConversionForIndex(op1):
                _, op1 = self.tmpVars.create_var_cached("tmpIndexTypeConv_", op1._dtype, def_val=op1)

            # if the op0 is not signal or other index index operator it is extracted
            # as tmp variable
            op0 = self.as_hdl_operand(op0)
            op0_t = ops[0]._dtype
            if isinstance(op0_t, HBits) and op0_t.bit_length() == 1 and not op0_t.force_vector:
                assert int(ops[1]) == 0, ops
                # drop whole index operator because it is useless
                return op0
            _op1 = self.as_hdl_HOperatorNode_indexRhs(op1)

            return HdlOp(HdlOpType.INDEX, [op0, _op1])

        elif o == HwtOps.TRUNC or o == HwtOps.SEXT or o == HwtOps.ZEXT:
            op0, op1 = ops
            op1 = int(op1)
            assert op1 >= 1, op
            resultSign = op.result._dtype.signed
            signedForVhdlResize = o == HwtOps.SEXT  # :note: VHDL std_numeric.resize supports only signed or unsinged
            if o == HwtOps.TRUNC:
                if isinstance(op0, RtlSignalBase) and isResultOfTypeConversionForIndex(op0):
                    _, op0 = self.tmpVars.create_var_cached("tmpTypeConv_", op0._dtype, def_val=op0)

                _op0 = self.as_hdl_operand(op0)
                if resultSign is None:
                    # prefer downto notation over resize with casts
                    _sliceOp = HdlOp(HdlOpType.DOWNTO, [self.as_hdl_int(int(op1) - 1), self.as_hdl_int(0)])
                    return HdlOp(HdlOpType.INDEX, [_op0, _sliceOp])
                signedForVhdlResize = resultSign  # it does not matter if trunc is signed/unsigned, but we preffer less casting
            else:
                _op0 = self.as_hdl_operand(op0)

            op0T = op0._dtype
            if op0T.signed is None and op0T.bit_length() == 1 and not op0T.force_vector and o != HwtOps.TRUNC:
                # use aggregate expression
                if o == HwtOps.SEXT:
                    msb = _op0
                else:
                    msb = self.as_hdl_HBitsConst(BIT.from_py(0))

                return [
                    HdlOp(HdlOpType.MAP_ASSOCIATION, [self.as_hdl_int(0), _op0]),
                    HdlOp(HdlOpType.MAP_ASSOCIATION, [HdlOthers, msb]),
                ]

            else:
                # use vhdl RESIZE()
                if resultSign != signedForVhdlResize:
                    _op0 = self.apply_cast(self._sign_flag_to_cast_id[signedForVhdlResize], _op0)

                _op1 = self.as_hdl_int(op1)
                res = hdl_call(self.RESIZE, [_op0, _op1])

                if resultSign != signedForVhdlResize:
                    res = self.apply_cast(self._sign_flag_to_cast_id[resultSign], res)

            return res

        elif o == HwtOps.TERNARY:
            _c, _op0, _op1 = ops
            op0 = self.as_hdl_cond(_c, True)
            op1 = self.as_hdl_operand(_op0)
            t0 = _op0._dtype
            t1 = _op1._dtype
            if not (t0 == t1):
                assert isinstance(t0, HBits) and\
                       isinstance(t1, HBits) and\
                       t0.bit_length() == t1.bit_length() and\
                       bool(t0.signed) == bool(t1.signed), (t0, t1)
                _, _op1 = self.tmpVars.create_var_cached("tmpTernaryAutoCast_", t0, def_val=_op1)

            op2 = self.as_hdl_operand(_op1)
            return HdlOp(HdlOpType.TERNARY, [op0, op1, op2])
        else:
            _o = self._cast_ops.get(o, None)
            if _o is not None:
                op0 = ops[0]
                op0 = self._as_Bits_vec(op0)
                if isinstance(op0, RtlSignalBase) and op0._isUnnamedExpr:
                    _, op0 = self.tmpVars.create_var_cached("tmpCastExpr_", op0._dtype, def_val=op0)
                return self.apply_cast(_o, self.as_hdl_operand(op0))

            _o = o.hdlConvertoAstOp
            if _o is None:
                o = self.op_transl_dict[o]
            else:
                vhldFn, isArithmetical = self.HDLCONVERTORAST_TO_VHDL.get(_o, (None, None))
                if vhldFn is not None:
                    op0, op1 = ops
                    _op0 = self.as_hdl_Value(op0)
                    op0Signed = op0._dtype.signed
                    if isArithmetical:
                        if not op0Signed:
                            _op0 = self.apply_cast(self.SIGNED, _op0)
                    else:
                        if op0Signed or op0Signed is None:
                            _op0 = self.apply_cast(self.UNSIGNED, _op0)

                    _op1 = self.as_hdl_HOperatorNode_indexRhs(op1)
                    res = hdl_call(vhldFn, [_op0, _op1])
                    resSigned = op.result._dtype.signed
                    if op0Signed != isArithmetical:
                        res = self.apply_cast(self._sign_flag_to_cast_id[resSigned], res)

                    return res
                o = _o

            if len(ops) == 2:
                res_t = op.result._dtype
                op0, op1 = ops

                zextMulMatch = False
                sextMulMatch = False
                if o == HdlOpType.MUL:
                    # optionally drop zext/sext and add casts
                    zextMulMatch, sextMulMatch, op0, op1 = matchFullWidthMul(op0, op1)

                if o != HdlOpType.CONCAT:
                    op0 = self._wrapConcatInTmpVariable(op0)
                    op1 = self._wrapConcatInTmpVariable(op1)

                if isinstance(res_t, HBits) and res_t != BOOL:
                    op0 = self._as_Bits(op0)
                    op1 = self._as_Bits(op1)

                _op0 = self.as_hdl_operand(op0)
                _op1 = self.as_hdl_operand(op1)
                if o == HdlOpType.EQ and isinstance(_op0, HdlValueId) and\
                        (isinstance(_op0.obj._dtype, HBits) and self._expandBitsOperandType(_op0.obj) == BOOL) and\
                        isinstance(_op1, HdlValueInt) and\
                        _op1.val:
                    # drop unnecessary casts
                    return _op0
                else:
                    assert o not in HDLCONVERTAST_OPS_SHIFT_AND_ROT, (o, "shifts and rotations should have been handled sooner in this function")
                    if o == HdlOpType.MUL and\
                            not sextMulMatch and\
                            not zextMulMatch and\
                            op0._dtype.strict_width and\
                            op1._dtype.strict_width:
                        return self._as_hdl_HOperatorNode_mulWithTrunc(op, op0._dtype, _op0, _op1)

                    return HdlOp(o, [_op0, _op1])

            return HdlOp(o, [self.as_hdl_operand(o2)
                             for o2 in ops])
