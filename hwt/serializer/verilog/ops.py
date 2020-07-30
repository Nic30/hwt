from typing import Union

from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOpType, HdlOp
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_call
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BIT, INT
from hwt.hdl.value import HValue
from hwt.serializer.exceptions import UnsupportedEventOpErr
from hwt.serializer.generic.ops import HWT_TO_HDLCONVEROTR_OPS
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class ToHdlAstVerilog_ops():
    SIGNED = HdlValueId("$signed", obj=LanguageKeyword())
    UNSIGNED = HdlValueId("$unsigned", obj=LanguageKeyword())
    op_transl_dict = {
        **HWT_TO_HDLCONVEROTR_OPS,
        AllOps.INDEX: HdlOpType.INDEX,
    }

    def _operandIsAnotherOperand(self, operand):
        if isinstance(operand, RtlSignal) and operand.hidden\
                and isinstance(operand.origin, Operator):
            return True

    def as_hdl_operand(self, operand: Union[RtlSignal, HValue], i: int,
                       operator: Operator):

        # [TODO] if operand is concatenation and parent operator
        #        is not concatenation operand should be extracted
        #        as tmp variable
        #        * maybe flatten the concatenations
        if operator.operator != AllOps.CONCAT\
                and self._operandIsAnotherOperand(operand)\
                and operand.origin.operator == AllOps.CONCAT:
            tmpVar = self.createTmpVarFn("tmp_concat_", operand._dtype)
            tmpVar.def_val = operand
            # Assignment(tmpVar, operand, virtual_only=True)
            operand = tmpVar

        oper = operator.operator
        width = None
        if operand._dtype == INT and\
           oper not in [AllOps.BitsAsUnsigned,
                        AllOps.BitsAsVec,
                        AllOps.BitsAsSigned,
                        AllOps.INDEX] and\
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
            return HdlOp(HdlOpType.APOSTROPHE, [self.as_hdl_int(width), hdl_op])
        else:
            return hdl_op

    def as_hdl_Operator(self, op: Operator):
        ops = op.operands
        o = op.operator

        if o == AllOps.TERNARY:
            zero, one = BIT.from_py(0), BIT.from_py(1)
            if ops[1] == one and ops[2] == zero:
                # ignore redundant x ? 1 : 0
                return self.as_hdl_cond(ops[0], True)
            else:
                op0 = self.as_hdl_cond(ops[0], True)
                op1 = self.as_hdl_operand(ops[1], 1, op)
                op2 = self.as_hdl_operand(ops[2], 2, op)
                return HdlOp(HdlOpType.TERNARY, [op0, op1, op2])
        elif o == AllOps.RISING_EDGE or o == AllOps.FALLING_EDGE:
            raise UnsupportedEventOpErr()
        elif o in [AllOps.BitsAsUnsigned, AllOps.BitsAsVec, AllOps.BitsAsSigned]:
            op0, = ops
            do_cast = bool(op0._dtype.signed) != bool(op.result._dtype.signed)

            op_hdl = self.as_hdl_operand(op0, 0, op)
            if do_cast:
                if bool(op0._dtype.signed):
                    cast = self.SIGNED
                else:
                    cast = self.UNSIGNED
                return hdl_call(cast, [op_hdl, ])
            else:
                return op_hdl
        else:
            _o = self.op_transl_dict[o]
            return HdlOp(_o, [self.as_hdl_operand(o2, i, op)
                              for i, o2 in enumerate(ops)])
