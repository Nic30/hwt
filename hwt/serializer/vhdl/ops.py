from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdl.operatorDefs import AllOps


# keep in mind that there is no such a thing in vhdl itself
opPrecedence = {AllOps.NOT: 2,
                AllOps.RISING_EDGE: 1,
                AllOps.NEG: 2,
                AllOps.DIV: 3,
                AllOps.ADD: 3,
                AllOps.SUB: 3,
                AllOps.MUL: 3,
                AllOps.XOR: 2,
                AllOps.EQ: 2,
                AllOps.NEQ: 2,
                AllOps.AND: 2,
                AllOps.OR: 2,
                AllOps.DOWNTO: 2,
                AllOps.GT: 2,
                AllOps.LT: 2,
                AllOps.GE: 2,
                AllOps.LE: 2,
                AllOps.CONCAT: 2,
                AllOps.INDEX: 1,
                AllOps.TERNARY: 1,
                AllOps.CALL: 1,
                }


def isResultOfTypeConversion(sig):
    try:
        sig.drivers[0]
    except IndexError:
        return False

    if sig.hidden:
        return True
    return False


class VhdlSerializer_ops():
    _binOps = {
        AllOps.AND: '%s AND %s',
        AllOps.OR: '%s OR %s',
        AllOps.XOR: '%s XOR %s',
        AllOps.CONCAT: '%s & %s',
        AllOps.DIV: '%s / %s',
        AllOps.DOWNTO: '%s-1 DOWNTO %s',
        AllOps.TO: '%s-1 TO %s',
        AllOps.EQ: '%s = %s',
        AllOps.GT: '%s > %s',
        AllOps.GE: '%s >= %s',
        AllOps.LE: '%s <= %s',
        AllOps.POW: '%s ** %s',
        AllOps.LT: '%s < %s',
        AllOps.SUB: '%s - %s',
        AllOps.MUL: '%s * %s',
        AllOps.NEQ: '%s /= %s',
        AllOps.ADD: '%s + %s',
    }
    _unaryOps = {
        AllOps.NOT: "NOT %s",
        AllOps.NEG: "-(%s)",
        AllOps.RISING_EDGE: "RISING_EDGE(%s)",
        AllOps.FALLIGN_EDGE: "FALLING_EDGE(%s)",
        AllOps.BitsAsSigned: "SIGNED(%s)",
        AllOps.BitsAsUnsigned: "UNSIGNED(%s)",
        AllOps.BitsAsVec: "STD_LOGIC_VECTOR(%s)",
    }

    @classmethod
    def _operand(cls, operand, operator, ctx):
        s = cls.asHdl(operand, ctx)
        if isinstance(operand, RtlSignalBase):
            try:
                o = operand.singleDriver()
                if o.operator != operator and\
                        opPrecedence[o.operator] <= opPrecedence[operator]:
                    return "(%s)" % s
            except Exception:
                pass
        return s

    @classmethod
    def _bin_op(cls, operator, op_str, ctx, ops):
        return op_str.join(map(lambda operand: cls._operand(operand, operator, ctx), ops))

    @classmethod
    def Operator(cls, op, ctx):
        # [TODO] no nested ternary in expressions like
        # ( '1'  WHEN r = f ELSE  '0' ) & "0"
        ops = op.operands
        o = op.operator

        op_str = cls._unaryOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], o, ctx))

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], o, ctx), cls._operand(ops[1], o, ctx))

        if o == AllOps.CALL:
            return "%s(%s)" % (cls.FunctionContainer(ops[0]),
                               ", ".join(map(lambda op: cls._operand(op, o, ctx), ops[1:])))
        elif o == AllOps.INDEX:
            assert len(ops) == 2
            o1 = ops[0]
            if isinstance(o1, RtlSignalBase) and isResultOfTypeConversion(o1):
                o1 = ctx.createTmpVarFn("tmpTypeConv", o1._dtype)
                o1.defaultVal = ops[0]

            return "%s(%s)" % (cls.asHdl(o1, ctx).strip(), cls._operand(ops[1], o, ctx))
        elif o == AllOps.TERNARY:
            return " ".join([cls._operand(ops[1], o, ctx), "WHEN",
                             cls.condAsHdl([ops[0]], True, ctx),
                             "ELSE",
                             cls._operand(ops[2], o, ctx)])
        elif o == AllOps.BitsToInt:
            assert len(ops) == 1
            op = cls.asHdl(ops[0], ctx)
            if ops[0]._dtype.signed is None:
                op = "UNSIGNED(%s)" % op
            return "TO_INTEGER(%s)" % op
        elif o == AllOps.IntToBits:
            assert len(ops) == 1
            resT = op.result._dtype
            op_str = cls.asHdl(ops[0], ctx)
            w = resT.bit_length()

            if resT.signed is None:
                return "STD_LOGIC_VECTOR(TO_UNSIGNED(%s, %d))" % (op_str, w)
            elif resT.signed:
                return "TO_UNSIGNED(%s, %d)" % (op_str, w)
            else:
                return "TO_UNSIGNED(%s, %d)" % (op_str, w)
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to vhdl" % (o))
