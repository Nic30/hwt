from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BIT, SLICE
from hwt.serializer.exceptions import UnsupportedEventOpErr


class ToHdlAstSystemC_ops():
    opPrecedence = {
        AllOps.NOT: 3,
        AllOps.MINUS_UNARY: 5,
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
        AllOps.BitsAsSigned: 2,
        AllOps.BitsAsUnsigned: 2,
        AllOps.BitsAsVec: 2,
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
            return op_str % (cls._operand(ops[0], 0, op, False, False, ctx))

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], 0, op, False, False, ctx),
                             cls._operand(ops[1], 1, op, False, False, ctx))

        if o == AllOps.INDEX:
            assert len(ops) == 2
            o0, o1 = ops
            o0_str = cls._operand(o0, 0, op, True, False, ctx)
            if ops[1]._dtype == SLICE:
                return "%s.range(%s, %s)" % (o0_str,
                                             # not operator i does not matter as they are all in ()
                                             cls._operand(o1.val.start, 1, op, False, True, ctx),
                                             cls._operand(o1.val.stop, 1, op, False, True, ctx))
            else:
                return "%s[%s]" % (o0_str, cls._operand(o1, 1, op, False, True, ctx))

        elif o == AllOps.TERNARY:
            zero, one = BIT.from_py(0), BIT.from_py(1)
            if ops[1] == one and ops[2] == zero:
                # ignore redundant x ? 1 : 0
                return cls.as_hdl_cond([ops[0]], True, ctx)
            else:
                return "%s ? %s : %s" % (cls.as_hdl_cond([ops[0]], True, ctx),
                                         cls._operand(ops[1], 1, op, False, False, ctx),
                                         cls._operand(ops[2], 2, op, False, False, ctx))
        elif o == AllOps.RISING_EDGE or o == AllOps.FALLING_EDGE:
            if ctx.isSensitivityList:
                if o == AllOps.RISING_EDGE:
                    _o = ".pos()"
                else:
                    _o = ".neg()"
                return cls._operand(ops[0], 0, op, True, False, ctx) + _o
            else:
                raise UnsupportedEventOpErr()
        elif o in [AllOps.BitsAsSigned, AllOps.BitsAsUnsigned,
                   AllOps.BitsAsVec]:
            assert len(ops) == 1
            return "static_cast<%s>(%s)" % (cls.HdlType(op.result._dtype, ctx),
                                            cls._operand(ops[0], 0, op, False, True, ctx))
        elif o == AllOps.POW:
            assert len(ops) == 2
            raise NotImplementedError()
            # return _bin('**')
        elif o == AllOps.CALL:
            return "%s(%s)" % (
                cls.FunctionContainer(ops[0]),
                ", ".join(map(lambda op: cls._operand(op, 1, op, False, True, ctx), ops[1:])))
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to vhdl" % (o))
