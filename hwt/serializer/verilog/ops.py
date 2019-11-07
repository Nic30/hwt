from typing import Union

from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BIT, INT
from hwt.hdl.value import Value
from hwt.serializer.exceptions import UnsupportedEventOpErr
from hwt.serializer.generic.context import SerializerCtx
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class VerilogSerializer_ops():
    # http://www.asicguru.com/verilog/tutorial/operators/57/
    opPrecedence = {
        AllOps.RISING_EDGE: 17,
        AllOps.FALLING_EDGE: 17,
        AllOps.TERNARY: 16,
        AllOps.AND: 11,
        AllOps.XOR: 11,
        AllOps.OR: 11,
        AllOps.EQ: 10,
        AllOps.NEQ: 10,
        AllOps.GT: 9,
        AllOps.LT: 9,
        AllOps.GE: 9,
        AllOps.LE: 9,
        AllOps.CONCAT: 5,
        AllOps.ADD: 7,
        AllOps.SUB: 7,
        AllOps.DIV: 6,
        AllOps.NEG: 5,
        AllOps.MUL: 3,
        AllOps.NOT: 3,
        AllOps.DOWNTO: 2,
        AllOps.TO: 2,
        AllOps.CALL: 2,
        AllOps.INDEX: 1,
        # AllOps.SHIFTL:8,
        # AllOps.SHIFTR:8,
        AllOps.BitsAsSigned: 1,
        AllOps.BitsAsUnsigned: 1,
        AllOps.BitsAsVec: 1,
    }
    _unaryOps = {
        AllOps.NOT: "~%s",
        AllOps.BitsAsSigned: "$signed(%s)",
        AllOps.BitsAsUnsigned: "$unsigned(%s)",
        AllOps.BitsAsVec: "%s",
    }

    _binOps = {
        AllOps.AND: '%s & %s',
        AllOps.OR: '%s | %s',
        AllOps.XOR: '%s ^ %s',
        AllOps.CONCAT: "{%s, %s}",
        AllOps.DIV: '%s / %s',
        AllOps.DOWNTO: '%s:%s',
        AllOps.TO: '%s:%s',
        AllOps.EQ: '%s == %s',
        AllOps.GT: '%s > %s',
        AllOps.GE: '%s >= %s',
        AllOps.LE: '%s <= %s',
        AllOps.LT: '%s < %s',
        AllOps.SUB: '%s - %s',
        AllOps.MUL: '%s * %s',
        AllOps.NEQ: '%s != %s',
        AllOps.ADD: '%s + %s',
        AllOps.POW: '%s ** %s',
    }

    @classmethod
    def _operandIsAnotherOperand(cls, operand):
        if isinstance(operand, RtlSignal) and operand.hidden\
                and isinstance(operand.origin, Operator):
            return True

    @classmethod
    def _operand(cls, operand: Union[RtlSignal, Value], i: int,
                 operator: Operator,
                 expr_requires_parenthesis: bool,
                 cancel_parenthesis: bool,
                 ctx: SerializerCtx):

        # [TODO] if operand is concatenation and parent operator
        #        is not concatenation operand should be extracted
        #        as tmp variable
        #        * maybe flatten the concatenations
        if operator.operator != AllOps.CONCAT\
                and cls._operandIsAnotherOperand(operand)\
                and operand.origin.operator == AllOps.CONCAT:
            tmpVar = ctx.createTmpVarFn("tmp_concat_", operand._dtype)
            tmpVar.def_val = operand
            # Assignment(tmpVar, operand, virtual_only=True)
            operand = tmpVar

        oper = operator.operator
        width = None
        if oper not in [AllOps.BitsAsUnsigned, AllOps.BitsAsVec,
                        AllOps.BitsAsSigned] and\
                oper is not AllOps.INDEX and\
                operand._dtype == INT and\
                operator.result is not None and\
                not operator.result._dtype == INT:
            # has to lock width
            for o in operator.operands:
                try:
                    bl = o._dtype.bit_length
                except AttributeError:
                    bl = None
                if bl is not None:
                    width = bl()
                    break

            assert width is not None, (operator, operand)

        s = super()._operand(operand, i, operator,
                             width is not None or expr_requires_parenthesis,
                             width is None and cancel_parenthesis, ctx)
        if width is not None:
            return "%d'%s" % (width, s)
        else:
            return s

    @classmethod
    def Operator(cls, op: Operator, ctx):
        ops = op.operands
        o = op.operator

        op_str = cls._unaryOps.get(o, None)
        if op_str is not None:
            cancel_parenthesis = op_str.endswith(")")
            return op_str % (cls._operand(ops[0], 0, op, False, cancel_parenthesis, ctx))

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            return cls._bin_op(op, op_str, ctx, cancel_parenthesis=o == AllOps.CONCAT)
        if o == AllOps.CALL:
            return "%s(%s)" % (
                cls.FunctionContainer(ops[0]),
                # operand i does not matter as they are all in ()
                ", ".join(map(lambda _op: cls._operand(_op, 1, op, False, True, ctx), ops[1:])))
        elif o == AllOps.INDEX:
            return cls._operator_index(op, ctx)
        elif o == AllOps.TERNARY:
            zero, one = BIT.from_py(0), BIT.from_py(1)
            if ops[1] == one and ops[2] == zero:
                # ignore redundant x ? 1 : 0
                return cls.condAsHdl([ops[0]], True, ctx)
            else:
                op0 = cls.condAsHdl([ops[0]], True, ctx)
                op1 = cls._operand(ops[1], op, False, False, ctx)
                op2 = cls._operand(ops[2], op, False, False, ctx)
                return "%s ? %s : %s" % (op0, op1, op2)
        elif o == AllOps.RISING_EDGE or o == AllOps.FALLING_EDGE:
            raise UnsupportedEventOpErr()
        elif o in [AllOps.BitsAsUnsigned, AllOps.BitsAsVec]:
            op0, = ops
            do_cast = bool(op0._dtype.signed)
            op_str = cls._operand(op0, op, False, do_cast, ctx)
            if do_cast:
                return "$unsigned(%s)" % op_str
            else:
                return op_str
        else:
            raise NotImplementedError(
                "Do not know how to convert expression with operator %s to verilog" % (o))
