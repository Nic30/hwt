from typing import Union

from hwt.code import If
from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL, INT
from hwt.hdl.value import Value
from hwt.serializer.generic.context import SerializerCtx
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


@internal
def isResultOfTypeConversion(sig):
    if len(sig.drivers) != 1:
        return False

    if sig.hidden:
        d = sig.singleDriver()
        return d.operator != AllOps.INDEX

    return False


class VhdlSerializer_ops():
    # keep in mind that there is no such a thing in vhdl itself
    opPrecedence = {
        AllOps.DOWNTO: 8,
        AllOps.TO: 8,
        AllOps.TERNARY: 8,

        AllOps.XOR: 7,
        AllOps.AND: 7,
        AllOps.OR: 7,

        AllOps.EQ: 6,
        AllOps.NEQ: 6,
        AllOps.GT: 6,
        AllOps.LT: 6,
        AllOps.GE: 6,
        AllOps.LE: 6,


        AllOps.CONCAT: 5,
        AllOps.ADD: 5,
        AllOps.SUB: 5,

        AllOps.NEG: 4,

        AllOps.DIV: 3,
        AllOps.MUL: 3,
        AllOps.MOD: 3,

        AllOps.NOT: 2,
        AllOps.POW: 2,

        AllOps.RISING_EDGE: 1,
        AllOps.FALLING_EDGE: 1,
        AllOps.INDEX: 1,
        AllOps.CALL: 1,
        AllOps.BitsAsSigned: 1,
        AllOps.BitsAsUnsigned: 1,
        AllOps.BitsAsVec: 1,
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
    def _operand(cls, operand: Union[RtlSignal, Value], i: int,
                 oper: Operator,
                 expr_requires_parenthesis: bool,
                 cancel_parenthesis: bool,
                 ctx: SerializerCtx):
        # no nested ternary in expressions like
        # ( '1'  WHEN r = f ELSE  '0' ) & "0"
        try:
            isTernaryOp = operand.hidden\
                and operand.drivers[0].operator == AllOps.TERNARY
        except (AttributeError, IndexError):
            isTernaryOp = False

        if isTernaryOp:
            # rewrite ternary operator as if
            operand = cls._tmp_var_for_ternary(operand, ctx)

        return super(VhdlSerializer_ops, cls)._operand(
                operand,
                i,
                oper,
                not isTernaryOp and expr_requires_parenthesis,
                isTernaryOp or cancel_parenthesis,
                ctx)

    @classmethod
    def Operator(cls, op: Operator, ctx: SerializerCtx):
        ops = op.operands
        o = op.operator

        op_str = cls._unaryOps.get(o, None)
        if op_str is not None:
            cancel_parenthesis = op_str[-1] == ")"
            return op_str % (cls._operand(ops[0], 0, op, False, cancel_parenthesis, ctx))

        op_str = cls._binOps.get(o, None)
        if op_str is not None:
            res_t = op.result._dtype
            if isinstance(res_t, Bits) and res_t != BOOL:
                op0 = cls._as_Bits(ops[0], ctx)
                op1 = cls._as_Bits(ops[1], ctx)
                op = op.operator._evalFn(op0, op1).drivers[0]
            return cls._bin_op(op, op_str, ctx, expr_requires_parenthesis=True)

        if o == AllOps.CALL:
            return "%s(%s)" % (
                cls.FunctionContainer(ops[0]),
                ", ".join(
                    # operand i does not matter as thy are all in ()
                    map(lambda op: cls._operand(op, 1, o, False, True, ctx), ops[1:])
                    )
                )
        elif o == AllOps.INDEX:
            op0, op1 = ops
            if isinstance(op0, RtlSignalBase) and isResultOfTypeConversion(op0):
                op0 = ctx.createTmpVarFn("tmpTypeConv", op0._dtype)
                op0.def_val = ops[0]

            # if the op0 is not signal or other index index operator it is extracted
            # as tmp variable
            op0_str = cls._operand(op0, 0, op, False, False, ctx)
            op1_str = cls._operand(ops[1], 1, op, False, True, ctx)

            if isinstance(op1._dtype, Bits) and op1._dtype != INT:
                sig = op1._dtype.signed
                if sig is None:
                    op1_str = "UNSIGNED(%s)" % op1_str
                op1_str = "TO_INTEGER(%s)" % op1_str

            return "%s(%s)" % (op0_str, op1_str)
        elif o == AllOps.TERNARY:
            op0 = cls.condAsHdl([ops[0]], True, ctx)
            op1 = cls._operand(ops[1], 1, op, False, False, ctx)
            op2 = cls._operand(ops[2], 2, op, False, False, ctx)
            return "%s WHEN %s ELSE %s" % (op0, op1, op2)
        else:
            raise NotImplementedError(
                "Do not know how to convert %s to vhdl" % (o))
