from hwt.hdl.operatorDefs import AllOps


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
        AllOps.AND: '%s._and__val(%s)',
        AllOps.OR: '%s._or__val(%s)',
        AllOps.XOR: '%s._xor__val(%s)',
        AllOps.CONCAT: "%s._concat__val(%s)",
        AllOps.DIV: '%s._floordiv__val(%s)',
        AllOps.DOWNTO: "SliceVal((%s, %s), SLICE, True)",
        AllOps.EQ: '%s._eq__val(%s)',
        AllOps.GT: '%s._gt__val(%s)',
        AllOps.GE: '%s._ge__val(%s)',
        AllOps.LE: '%s._le__val(%s)',
        AllOps.LT: '%s._lt__val(%s)',
        AllOps.SUB: '%s._sub__val(%s)',
        AllOps.MUL: '%s._mul__val(%s)',
        AllOps.NEQ: '%s._ne__val(%s)',
        AllOps.ADD: '%s._add__val(%s)',
        AllOps.POW: "power(%s, %s)",
    }
    _unaryOps = {
        AllOps.NOT: "(%s)._invert__val()",
        AllOps.RISING_EDGE: "(%s)._onRisingEdge__val(sim.now)",
        AllOps.FALLIGN_EDGE: "(%s)._onFallingEdge__val(sim.now)",
        AllOps.BitsAsSigned: "(%s)._convSign__val(True)",
        AllOps.BitsAsUnsigned: "(%s)._convSign__val(False)",
        AllOps.BitsAsVec: "(%s)._convSign__val(None)",
        AllOps.NEG: "(%s)._neg__val()",
    }

    @classmethod
    def Operator(cls, op, ctx):
        ops = op.operands
        o = op.operator

        op_str = cls._unaryOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], o, ctx))

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], o, ctx),
                             cls._operand(ops[1], o, ctx))

        if o == AllOps.INDEX:
            assert len(ops) == 2
            return "(%s)._getitem__val(%s)" % (cls.asHdl(ops[0], ctx),
                                               cls._operand(ops[1], o, ctx))
        elif o == AllOps.TERNARY:
            return "(%s)._ternary__val(%s, %s)" %\
                tuple(map(lambda x: cls.asHdl(x, ctx), ops))
        elif o == AllOps.BitsToInt:
            assert len(ops) == 1
            op = ops[0]
            return "convertSimBits__val(%s, %s, SIM_INT)" % (
                cls.HdlType_bits(op._dtype, ctx),
                cls.asHdl(op, ctx))
        elif o == AllOps.IntToBits:
            assert len(ops) == 1
            resT = op.result._dtype
            return "convertSimInteger__val(%s, %s, %s)" % (
                cls.HdlType(ops[0]._dtype, ctx),
                cls.asHdl(
                    ops[0], ctx),
                cls.HdlType_bits(resT, ctx))
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to simModel" % (o))
