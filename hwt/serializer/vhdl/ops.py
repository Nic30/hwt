from typing import Union

from hwt.code import If
from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps, OpDefinition
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, INT
from hwt.hdl.value import Value
from hwt.serializer.generic.context import SerializerCtx
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


@internal
def isResultOfTypeConversion(sig):
    if not sig.drivers:
        return False

    if sig.hidden:
        return True

    return False


class VhdlSerializer_ops():
    # keep in mind that there is no such a thing in vhdl itself
    opPrecedence = {
        AllOps.NOT: 2,
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
        AllOps.FALLING_EDGE: "FALLING_EDGE(%s)",
        AllOps.BitsAsSigned: "SIGNED(%s)",
        AllOps.BitsAsUnsigned: "UNSIGNED(%s)",
        AllOps.BitsAsVec: "STD_LOGIC_VECTOR(%s)",
    }

    @internal
    @classmethod
    def _tmp_var_for_ternary(cls, val: RtlSignal, ctx: SerializerCtx):
        """
        Optionaly convert boolean to std_logic_vector
        """
        o = ctx.createTmpVarFn("tmpTernary", val._dtype)
        cond, ifTrue, ifFalse = val.drivers[0].operands
        if_ = If(cond)
        if_.ifTrue.append(Assignment(ifTrue, o,
                                     virtual_only=True,
                                     parentStm=if_))
        if_.ifFalse = []
        if_.ifFalse.append(Assignment(ifFalse, o,
                                      virtual_only=True,
                                      parentStm=if_))
        if_._outputs.append(o)
        for obj in (cond, ifTrue, ifFalse):
            if isinstance(obj, RtlSignalBase):
                if_._inputs.append(obj)
        o.drivers.append(if_)
        return o

    @classmethod
    def _as_Bits(cls, val: Union[RtlSignal, Value], ctx: SerializerCtx):
        if val._dtype == BOOL:
            bit1_t = Bits(1)
            o = ctx.createTmpVarFn("tmpBool2std_logic", bit1_t)
            ifTrue, ifFalse = bit1_t.from_py(1), bit1_t.from_py(0)
            if_ = If(val)
            if_.ifTrue.append(Assignment(ifTrue, o, virtual_only=True, parentStm=if_))
            if_.ifFalse = []
            if_.ifFalse.append(Assignment(ifFalse, o, virtual_only=True, parentStm=if_))
            if_._outputs.append(o)
            o.drivers.append(if_)
            return o
        else:
            assert isinstance(val._dtype, Bits), val._dtype
            return val

    @internal
    @classmethod
    def _operand(cls, operand: Union[RtlSignal, Value],
                 operator: OpDefinition,
                 ctx: SerializerCtx):
        try:
            isTernaryOp = operand.hidden\
                and operand.drivers[0].operator == AllOps.TERNARY
        except (AttributeError, IndexError):
            isTernaryOp = False

        if isTernaryOp:
            # rewrite ternary operator as if
            operand = cls._tmp_var_for_ternary(operand, ctx)

        s = cls.asHdl(operand, ctx)
        if isinstance(operand, RtlSignalBase):
            try:
                o = operand.singleDriver()
                if o.operator != operator and\
                        cls.opPrecedence[o.operator] <= cls.opPrecedence[operator]:
                    return "(%s)" % s
            except Exception:
                pass
        return s

    @classmethod
    def Operator(cls, op: Operator, ctx: SerializerCtx):
        # [TODO] no nested ternary in expressions like
        # ( '1'  WHEN r = f ELSE  '0' ) & "0"
        ops = op.operands
        o = op.operator

        op_str = cls._unaryOps.get(o, None)
        if op_str is not None:
            return op_str % (cls._operand(ops[0], o, ctx))

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            res_t = op.result._dtype
            op0, op1 = ops
            if isinstance(res_t, Bits) and res_t != BOOL:
                op0 = cls._as_Bits(op0, ctx)
                op1 = cls._as_Bits(op1, ctx)

            return op_str % (cls._operand(op0, o, ctx),
                             cls._operand(op1, o, ctx))

        if o == AllOps.CALL:
            return "%s(%s)" % (
                cls.FunctionContainer(ops[0]),
                ", ".join(
                    map(lambda op: cls._operand(op, o, ctx), ops[1:])
                    )
                )
        elif o == AllOps.INDEX:
            op0, op1 = ops
            if isinstance(op0, RtlSignalBase) and isResultOfTypeConversion(op0):
                op0 = ctx.createTmpVarFn("tmpTypeConv", op0._dtype)
                op0.def_val = ops[0]

            op0_str = cls.asHdl(op0, ctx).strip()
            op1_str = cls._operand(ops[1], o, ctx)
            if isinstance(op1._dtype, Bits) and op1._dtype != INT:
                sig = op1._dtype.signed
                if sig is None:
                    op1_str = "UNSIGNED(%s)" % op1_str
                op1_str = "TO_INTEGER(%s)" % op1_str

            return "%s(%s)" % (op0_str, op1_str)
        elif o == AllOps.TERNARY:
            return " ".join([cls._operand(ops[1], o, ctx), "WHEN",
                             cls.condAsHdl([ops[0]], True, ctx),
                             "ELSE",
                             cls._operand(ops[2], o, ctx)])
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to vhdl" % (o))
