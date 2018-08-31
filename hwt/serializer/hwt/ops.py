from hwt.hdl.operatorDefs import AllOps
from hwt.serializer.hwt.context import HwtSerializerCtx


class HwtSerializer_ops():
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
        AllOps.AND: '%s & %s',
        AllOps.OR: '%s | %s',
        AllOps.XOR: '%s ^ %s',
        AllOps.CONCAT: "Concat(%s, %s)",
        AllOps.DIV: '%s / %s',
        AllOps.DOWNTO: "%s:%s",
        AllOps.EQ: '%s._eq(%s)',
        AllOps.GT: '%s > %s',
        AllOps.GE: '%s >= %s',
        AllOps.LE: '%s <= %s',
        AllOps.LT: '%s < %s',
        AllOps.SUB: '%s - %s',
        AllOps.MUL: '%s * %s',
        AllOps.NEQ: '%s != %s',
        AllOps.ADD: '%s + %s',
        AllOps.POW: "power(%s, %s)",
    }
    _unaryOps = {
        AllOps.NOT: "~%s",
        AllOps.NEG: "-%s",
        AllOps.RISING_EDGE: "(%s)._onRisingEdge()",
        AllOps.FALLING_EDGE: "(%s)._onFallingEdge()",
    }
    _castOps = {
        AllOps.BitsAsSigned,
        AllOps.BitsAsUnsigned,
        AllOps.BitsAsVec,
        AllOps.BitsToInt,
    }

    @classmethod
    def Operator(cls, op, ctx: HwtSerializerCtx):
        ops = op.operands
        o = op.operator
        
        asHdl = cls.asHdl

        with ctx.valWidthReq(o == AllOps.CONCAT):
            op_str = cls._unaryOps.get(o, None)
            if op_str is not None:
                    return op_str % (cls._operand(ops[0], o, ctx))
    
            op_str = cls._binOps.get(o, None)
            if op_str is not None:
                return op_str % (cls._operand(ops[0], o, ctx),
                                 cls._operand(ops[1], o, ctx))
    
            if o in cls._castOps:
                return "(%s)._reinterpret_cast(%s)" % (asHdl(ops[0], ctx),
                                                       cls.HdlType(op.result._dtype, ctx))
    
            if o == AllOps.INDEX:
                assert len(ops) == 2
                return "(%s)[%s]" % (asHdl(ops[0], ctx),
                                     cls._operand(ops[1], o, ctx))
            elif o == AllOps.TERNARY:
                res, op0, op1 = ops
                resStr = asHdl(res, ctx)
                with ctx.valWidthReq(True):
                    op0Str = asHdl(op0, ctx)
                    op1Str = asHdl(op1, ctx)
                return "(%s)._ternary(%s, %s)" % (resStr, op0Str, op1Str)
            elif o == AllOps.BitsToInt:
                assert len(ops) == 1
                op = ops[0]
                return "%s.auto_cast(INT)" % (
                    asHdl(op, ctx))
            elif o == AllOps.IntToBits:
                assert len(ops) == 1
                resT = op.result._dtype
                return "%s.auto_cast(%s)" % (
                    asHdl(ops[0], ctx),
                    cls.HdlType_bits(resT, ctx))
            else:
                raise NotImplementedError(
                    "Do not know how to convert %s to simModel" % (o))
