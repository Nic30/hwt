from hwt.hdl.operatorDefs import AllOps
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class SimModelSerializer_ops():
    opPrecedence = {
        AllOps.NOT: 4,
        AllOps.NEG: 4,
        AllOps.RISING_EDGE: 1,
        AllOps.DIV: 4,
        AllOps.ADD: 5,
        AllOps.SUB: 5,
        AllOps.MUL: 4,
        AllOps.XOR: 9,
        AllOps.EQ: 10,
        AllOps.NEQ: 10,
        AllOps.AND: 10,
        AllOps.OR: 10,
        AllOps.DOWNTO: 1,
        AllOps.GT: 10,
        AllOps.LT: 10,
        AllOps.GE: 10,
        AllOps.LE: 10,
        AllOps.CONCAT: 1,
        AllOps.INDEX: 1,
        AllOps.TERNARY: 1,
        AllOps.CALL: 1,
    }
    _binOps = {
        AllOps.AND: '(%s) & (%s)',
        AllOps.OR: '(%s) | (%s)',
        AllOps.XOR: '(%s) ^ (%s)',
        AllOps.CONCAT: "(%s)._concat(%s)",
        AllOps.DIV: '(%s) // (%s)',
        AllOps.DOWNTO: "slice(%s, %s)",
        AllOps.EQ: '(%s)._eq(%s)',
        AllOps.GT: '(%s) > (%s)',
        AllOps.GE: '(%s) >= (%s)',
        AllOps.LE: '(%s) <= (%s)',
        AllOps.LT: '(%s) < (%s)',
        AllOps.SUB: '(%s) - (%s)',
        AllOps.MUL: '(%s) * (%s)',
        AllOps.NEQ: '(%s) != (%s)',
        AllOps.ADD: '(%s) + (%s)',
        AllOps.POW: "(%s) ** (%s)",
    }
    _unaryEventOps = {
        AllOps.RISING_EDGE: "%s._onRisingEdge()",
        AllOps.FALLING_EDGE: "%s._onFallingEdge()",
    }
    _unaryOps = {
        AllOps.NOT: "(%s).__invert__()",
        AllOps.NEG: "(%s).__neg__()",

        AllOps.BitsAsSigned: "%s.cast_sign(True)",
        AllOps.BitsAsUnsigned: "(%s).cast_sign(False)",
        AllOps.BitsAsVec: "(%s).cast_sign(False)",
    }

    @classmethod
    def Operator(cls, op, ctx):
        ops = op.operands
        o = op.operator

        op_str = cls._unaryOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], o, ctx))
        op_str = cls._unaryEventOps.get(o, None)
        if op_str is not None:
            op0 = ops[0]
            assert isinstance(op0, RtlSignal) and not op0.hidden, op0
            return op_str % ("self.io.%s" % op0.name)

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], o, ctx),
                             cls._operand(ops[1], o, ctx))

        if o == AllOps.INDEX:
            assert len(ops) == 2
            return "(%s)[%s]" % (cls.asHdl(ops[0], ctx),
                                 cls._operand(ops[1], o, ctx))
        elif o == AllOps.TERNARY:
            return "(%s)._ternary__val(%s, %s)" %\
                tuple(map(lambda x: cls.asHdl(x, ctx), ops))
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to simModel" % (o))
