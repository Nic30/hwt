from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BIT
from hwt.serializer.exceptions import UnsupportedEventOpErr
from hwt.hdl.value import Value
from hwt.hdl.operator import Operator
from hwt.serializer.generic.context import SerializerCtx
from hwt.hdl.types.integer import Integer
from typing import Union
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.hdl.assignment import Assignment


class VerilogSerializer_ops():
    # http://www.asicguru.com/verilog/tutorial/operators/57/
    opPrecedence = {
        AllOps.NOT: 3,
        AllOps.NEG: 5,
        AllOps.RISING_EDGE: 0,
        AllOps.DIV: 6,
        AllOps.ADD: 7,
        AllOps.SUB: 7,
        AllOps.MUL: 3,
        AllOps.EQ: 10,
        AllOps.NEQ: 10,
        AllOps.AND: 11,
        AllOps.XOR: 11,
        AllOps.OR: 11,
        AllOps.DOWNTO: 2,
        AllOps.GT: 9,
        AllOps.LT: 9,
        AllOps.GE: 9,
        AllOps.LE: 9,
        AllOps.CONCAT: 5,
        AllOps.INDEX: 1,
        AllOps.TERNARY: 16,
        AllOps.CALL: 2,
        # AllOps.SHIFTL:8,
        # AllOps.SHIFTR:8,
        # AllOps.DOWNTO:
        # AllOps.TO:
    }
    _unaryOps = {
        AllOps.NOT: "~%s",
        AllOps.BitsAsSigned: "$signed(%s)",
        AllOps.BitsToInt: "%s",
        #AllOps.IntToBits: "%s",
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
    def _operand(cls, operand: Union[RtlSignal, Value],
                 operator: Operator, ctx: SerializerCtx):

        # [TODO] if operand is concatenation and parent operator
        #        is not concatenation operand should be extracted
        #        as tmp variable
        #        * maybe flatten the concatenations
        if operator.operator != AllOps.CONCAT and cls._operandIsAnotherOperand(operand)\
                and operand.origin.operator == AllOps.CONCAT:
            tmpVar = ctx.createTmpVarFn("tmp_concat_", operand._dtype)
            tmpVar.defVal = operand
            # Assignment(tmpVar, operand, virtualOnly=True)
            operand = tmpVar

        s = super()._operand(operand, operator.operator, ctx)
        oper = operator.operator
        if oper not in [AllOps.BitsAsUnsigned, AllOps.BitsAsVec,
                        AllOps.IntToBits, AllOps.BitsAsSigned] and \
                oper is not AllOps.INDEX and\
                isinstance(operand._dtype, Integer) and\
                operator.result is not None and\
                not isinstance(operator.result._dtype, Integer):
            # has to lock width
            width = None
            for o in operator.operands:
                try:
                    bl = o._dtype.bit_length
                except AttributeError:
                    bl = None
                if bl is not None:
                    width = bl()
                    break

            assert width is not None, (operator, operand)
            if s.startswith("("):
                return "%d'%s" % (width, s)
            else:
                return "%d'(%s)" % (width, s)

        return s

    @classmethod
    def Operator(cls, op: Operator, ctx):
        ops = op.operands
        o = op.operator

        op_str = cls._unaryOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], op, ctx))

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], op, ctx),
                             cls._operand(ops[1], op, ctx))

        if o == AllOps.CALL:
            return "%s(%s)" % (cls.FunctionContainer(ops[0]),
                               ", ".join(map(lambda _op: cls._operand(_op, op, ctx), ops[1:])))
        elif o == AllOps.INDEX:
            assert len(ops) == 2
            o1 = ops[0]
            return "%s[%s]" % (cls._operand(o1, op, ctx),
                               cls._operand(ops[1], op, ctx))
        elif o == AllOps.TERNARY:
            zero, one = BIT.fromPy(0), BIT.fromPy(1)
            if ops[1] == one and ops[2] == zero:
                # ignore redundant x ? 1 : 0
                return cls.condAsHdl([ops[0]], True, ctx)
            else:
                return "%s ? %s : %s" % (cls.condAsHdl([ops[0]], True, ctx),
                                         cls._operand(ops[1], op, ctx),
                                         cls._operand(ops[2], op, ctx))
        elif o == AllOps.RISING_EDGE or o == AllOps.FALLING_EDGE:
            raise UnsupportedEventOpErr()
        elif o in [AllOps.BitsAsUnsigned, AllOps.BitsAsVec]:
            op0, = ops
            op_str = cls._operand(op0, op, ctx)
            if bool(op0._dtype.signed):
                return "$unsigned(%s)" % op_str
            else:
                return op_str
        elif o == AllOps.IntToBits:
            op0, = ops
            width = op.result._dtype.bit_length()
            op_str = cls._operand(op0, op, ctx)
            if op_str.startswith("(") and not isinstance(op, Value):
                return "%d'%s" % (width, op_str)
            else:
                return "%d'(%s)" % (width, op_str)
        else:
            raise NotImplementedError(
                "Do not know how to convert expression with operator %s to verilog" % (o))
