from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BIT, SLICE
from hwt.serializer.exceptions import UnsupportedEventOpErr


class SystemCSerializer_ops():
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
        AllOps.XOR: 12,
        AllOps.OR: 13,
        AllOps.DOWNTO: 2,
        AllOps.TO: 2,
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
    }

    _unaryOps = {
        AllOps.NOT: "~%s",
    }

    _binOps = {
        AllOps.AND: '%s & %s',
        AllOps.OR: '%s | %s',
        AllOps.XOR: '%s ^ %s',
        AllOps.CONCAT: '%s & %s',
        AllOps.DIV: '%s / %s',
        AllOps.EQ: '%s == %s',
        AllOps.NEQ: '%s != %s',
        AllOps.GT: '%s > %s',
        AllOps.LT: '%s < %s',
        AllOps.GE: '%s >= %s',
        AllOps.LE: '%s <= %s',
        AllOps.SUB: '%s - %s',
        AllOps.MUL: '%s * %s',
        AllOps.ADD: '%s + %s',
    }
    #  AllOps.DOWNTO:  '%s:%s',
    #  AllOps.TO: '%s:%s'

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
            o0, o1 = ops
            o0_str = cls.asHdl(o0, ctx)
            if ops[1]._dtype == SLICE:
                return "%s.range(%s, %s)" % (o0_str,
                                             cls._operand(o1.val.start, o, ctx),
                                             cls._operand(o1.val.stop, o, ctx))
            else:
                return "%s[%s]" % (o0_str, cls._operand(o1, o, ctx))

        elif o == AllOps.TERNARY:
            zero, one = BIT.from_py(0), BIT.from_py(1)
            if ops[1] == one and ops[2] == zero:
                # ignore redundant x ? 1 : 0
                return cls.condAsHdl([ops[0]], True, ctx)
            else:
                return "%s ? %s : %s" % (cls.condAsHdl([ops[0]], True, ctx),
                                         cls._operand(ops[1], o, ctx),
                                         cls._operand(ops[2], o, ctx))
        elif o == AllOps.RISING_EDGE or o == AllOps.FALLING_EDGE:
            if ctx.isSensitivityList:
                if o == AllOps.RISING_EDGE:
                    _o = ".pos()"
                else:
                    _o = ".neg()"
                return cls._operand(ops[0], o, ctx) + _o
            else:
                raise UnsupportedEventOpErr()
        elif o in [AllOps.BitsAsSigned, AllOps.BitsAsUnsigned,
                   AllOps.BitsAsVec]:
            assert len(ops) == 1
            return "static_cast<%s>(%s)" % (cls.HdlType(op.result._dtype, ctx),
                                            cls._operand(ops[0], o, ctx))
        elif o == AllOps.POW:
            assert len(ops) == 2
            raise NotImplementedError()
            # return _bin('**')
        elif o == AllOps.CALL:
            return "%s(%s)" % (cls.FunctionContainer(ops[0]),
                               ", ".join(map(lambda op: cls._operand(op, o, ctx), ops[1:])))
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to vhdl" % (o))
