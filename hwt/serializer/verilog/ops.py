from builtins import isinstance
from typing import Union

from hdlConvertorAst.hdlAst import HdlValueInt
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOpType, HdlOp
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call
from hwt.hdl.commonConstants import b1, b0
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import INT, SLICE
from hwt.serializer.exceptions import UnsupportedEventOpErr
from hwt.serializer.generic.ops import HWT_TO_HDLCONVERTOR_OPS
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.serializer.vhdl.ops import matchFullWidthMul


class ToHdlAstVerilog_ops():
    SIGNED = HdlValueId("$signed", obj=LanguageKeyword())
    UNSIGNED = HdlValueId("$unsigned", obj=LanguageKeyword())
    op_transl_dict = {
        **HWT_TO_HDLCONVERTOR_OPS,
        HwtOps.INDEX: HdlOpType.INDEX,
    }

    def _operandIsAnotherOperand(self, operand):
        if isinstance(operand, RtlSignal) and operand._isUnnamedExpr\
                and isinstance(operand._rtlObjectOrigin, HOperatorNode):
            return True

    def as_hdl_operand(self, operand: Union[RtlSignal, HConst], i: int,
                       operator: HOperatorNode):

        # [TODO] if operand is concatenation and parent operator
        #        is not concatenation operand should be extracted
        #        as tmp variable
        #        * maybe flatten the concatenations
        if operator.operator != HwtOps.CONCAT\
                and self._operandIsAnotherOperand(operand)\
                and operand._rtlObjectOrigin.operator == HwtOps.CONCAT:
            _, tmpVar = self.tmpVars.create_var_cached("tmp_concat_", operand._dtype, def_val=operand)
            # HdlAssignmentContainer(tmpVar, operand, virtual_only=True)
            operand = tmpVar
        elif operator.operator in (HwtOps.INDEX, HwtOps.TRUNC) and i == 0 and self._operandIsAnotherOperand(operand):
            tmpVarName = "tmp_index_" if operator.operator == HwtOps.INDEX else "tmp_trunc_"
            _, tmpVar = self.tmpVars.create_var_cached(tmpVarName, operand._dtype, def_val=operand)
            operand = tmpVar
        elif self._operandIsAnotherOperand(operand)\
                and operand._rtlObjectOrigin.operator == HwtOps.MUL:
            _, tmpVar = self.tmpVars.create_var_cached("tmp_mul_", operand._dtype, def_val=operand)
            operand = tmpVar

        oper = operator.operator
        width = None
        if not isinstance(operand, RtlSignal) and operand._dtype == INT and\
           oper not in [HwtOps.BitsAsUnsigned,
                        HwtOps.BitsAsVec,
                        HwtOps.BitsAsSigned,
                        HwtOps.INDEX] and\
                operator.result is not None and\
                not operator.result._dtype == INT:
            # have to lock the width
            for o in operator.operands:
                try:
                    bl = o._dtype.bit_length
                except AttributeError:
                    bl = None
                if bl is not None:
                    width = bl()
                    break

            assert width is not None, (operator, operand)

        hdl_op = self.as_hdl_Value(operand)
        if width is not None:
            if isinstance(hdl_op, HdlValueInt):
                assert isinstance(width, int), width
                hdl_op.bits = width
            else:
                return HdlOp(HdlOpType.APOSTROPHE, [self.as_hdl_int(width), hdl_op])
        return hdl_op

    def as_hdl_HOperatorNode(self, op: HOperatorNode):
        ops = op.operands
        o = op.operator

        if o == HwtOps.TERNARY:
            if ops[1] == b1 and ops[2] == b0:
                # ignore redundant x ? 1 : 0
                return self.as_hdl_cond(ops[0], True)
            else:
                op0 = self.as_hdl_cond(ops[0], True)
                op1 = self.as_hdl_operand(ops[1], 1, op)
                op2 = self.as_hdl_operand(ops[2], 2, op)
                return HdlOp(HdlOpType.TERNARY, [op0, op1, op2])
        elif o == HwtOps.RISING_EDGE or o == HwtOps.FALLING_EDGE:
            raise UnsupportedEventOpErr()
        elif o in (HwtOps.BitsAsUnsigned, HwtOps.BitsAsVec, HwtOps.BitsAsSigned):
            op0, = ops
            do_cast = bool(op0._dtype.signed) != bool(op.result._dtype.signed)

            op_hdl = self.as_hdl_operand(op0, 0, op)
            if do_cast:
                if bool(op.result._dtype.signed):
                    cast = self.SIGNED
                else:
                    cast = self.UNSIGNED
                return hdl_call(cast, [op_hdl, ])
            else:
                return op_hdl

        elif o == HwtOps.TRUNC:
            # convert trunc to slice
            resWidth = int(ops[1])
            return HdlOp(HdlOpType.INDEX, [
                self.as_hdl_operand(ops[0], 0, op),
                self.as_hdl_HSliceConst(SLICE.from_py(slice(resWidth, 0, -1)))
            ])
        elif o in (HwtOps.SEXT, HwtOps.ZEXT):
            # convert sext to concat with repliacation, zext to concat 0
            # x4b._sext(8) -> { {8-4{x[4-1]}}, x }; # replication operator
            resWidth = int(ops[1])
            srcWidth = ops[0]._dtype.bit_length()
            prefixLen = resWidth - srcWidth
            if o == HwtOps.ZEXT:
                prefix = self.as_hdl_HBitsConst(HBits(prefixLen).from_py(0))
            else:
                if srcWidth == 1:
                    msb = self.as_hdl_operand(ops[0], 0, op)
                else:
                    msb = HdlOp(HdlOpType.INDEX, [
                        self.as_hdl_operand(ops[0], 0, op),
                        self.as_hdl_int(srcWidth - 1),
                    ])
                if prefixLen == 1:
                    prefix = msb
                else:
                    prefix = HdlOp(HdlOpType.REPL_CONCAT, [
                        self.as_hdl_int(prefixLen),
                        msb,
                    ])
            return HdlOp(HdlOpType.CONCAT, [
                prefix,
                self.as_hdl_operand(ops[0], 0, op)
            ])

        else:
            if o == HwtOps.MUL:
                op0, op1 = ops
                # optionally drop zext/sext and add casts
                _, _, op0, op1 = matchFullWidthMul(op0, op1)
                ops = [op0, op1]
            elif o == HwtOps.INDEX:
                op0_t = ops[0]._dtype
                if isinstance(op0_t, HBits) and op0_t.bit_length() == 1 and not op0_t.force_vector:
                    assert int(ops[1]) == 0, ops
                    # drop whole index operator when indexing on 1b vector
                    return self.as_hdl_operand(ops[0], 0, op)

            _o = self.op_transl_dict[o]
            return HdlOp(_o, [self.as_hdl_operand(o2, i, op)
                              for i, o2 in enumerate(ops)])
