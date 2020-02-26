from hwt.hdl.operatorDefs import AllOps
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class SimModelSerializer_ops():
    opPrecedence = {
        AllOps.RISING_EDGE: 1,
        AllOps.FALLING_EDGE: 1,
        AllOps.DOWNTO: 1,
        AllOps.TO: 1,

        AllOps.EQ: 11,
        AllOps.NEQ: 11,
        AllOps.GT: 11,
        AllOps.LT: 11,
        AllOps.GE: 11,
        AllOps.LE: 11,

        AllOps.OR: 10,
        AllOps.XOR: 9,
        AllOps.AND: 8,

        AllOps.ADD: 6,
        AllOps.SUB: 6,

        AllOps.DIV: 5,
        AllOps.MUL: 5,
        AllOps.MOD: 5,

        AllOps.NOT: 4,
        AllOps.NEG: 4,
        AllOps.POW: 3,
        AllOps.INDEX: 2,

        AllOps.CONCAT: 1,
        AllOps.TERNARY: 1,
        AllOps.CALL: 1,
        AllOps.BitsAsSigned: 1,
        AllOps.BitsAsUnsigned: 1,
        AllOps.BitsAsVec: 1,
    }
    _binOps = {
        AllOps.AND: '%s & %s',
        AllOps.OR: '%s | %s',
        AllOps.XOR: '%s ^ %s',
        AllOps.CONCAT: "%s._concat(%s)",
        AllOps.DIV: '%s // %s',
        AllOps.DOWNTO: "slice(%s, %s)",
        AllOps.EQ: '%s._eq(%s)',
        AllOps.GT: '%s > %s',
        AllOps.GE: '%s >= %s',
        AllOps.LE: '%s <= %s',
        AllOps.LT: '%s < %s',
        AllOps.SUB: '%s - %s',
        AllOps.MUL: '%s * %s',
        AllOps.NEQ: '%s != %s',
        AllOps.ADD: '%s + %s',
        AllOps.POW: "%s ** %s",
    }
    _unaryEventOps = {
        AllOps.RISING_EDGE: "%s._onRisingEdge()",
        AllOps.FALLING_EDGE: "%s._onFallingEdge()",
    }
    _unaryOps = {
        AllOps.NOT: "~%s",
        AllOps.NEG: "-%s",

        AllOps.BitsAsSigned: "%s.cast_sign(True)",
        AllOps.BitsAsUnsigned: "%s.cast_sign(False)",
        AllOps.BitsAsVec: "%s.cast_sign(False)",
    }

    @classmethod
    def Operator(cls, op, ctx):
        ops = op.operands
        o = op.operator

        op_str = cls._unaryOps.get(o, None)
        if op_str is not None:
            requires_braces = op_str[2] == "."
            op0 = cls._operand(ops[0], 0, op, requires_braces, False, ctx)
            return op_str % (op0)
        op_str = cls._unaryEventOps.get(o, None)
        if op_str is not None:
            op0 = ops[0]
            assert isinstance(op0, RtlSignal) and not op0.hidden, op0
            return op_str % ("self.io.%s" % op0.name)

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            return cls._bin_op(op, op_str, ctx)

        if o == AllOps.INDEX:
            return cls._operator_index(op, ctx)
        elif o == AllOps.TERNARY:
            op0 = cls._operand(ops[0], 0, op, True, False, ctx)
            op1 = cls._operand(ops[1], 1, op, False, True, ctx)
            op2 = cls._operand(ops[2], 2, op, False, True, ctx)
            return "%s._ternary__val(%s, %s)" % (op0, op1, op2)
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to simModel" % (o))
