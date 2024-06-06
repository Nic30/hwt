from hdlConvertorAst.hdlAst._expr import HdlOpType
from hwt.hdl.operatorDefs import HwtOps


HWT_TO_HDLCONVERTOR_OPS = {
    **{op: getattr(HdlOpType, op.id) for op in [
        HwtOps.AND,
        HwtOps.OR,
        HwtOps.XOR,
        HwtOps.CONCAT,
        HwtOps.DIV,
        HwtOps.DOWNTO,
        HwtOps.TO,
        HwtOps.EQ,
        HwtOps.GT,
        HwtOps.GE,
        HwtOps.LE,
        HwtOps.POW,
        HwtOps.LT,
        HwtOps.SUB,
        HwtOps.MUL,
        HwtOps.NE,
        HwtOps.ADD,
        HwtOps.TERNARY,
    ]},
    HwtOps.UDIV: HdlOpType.DIV,
    HwtOps.SDIV: HdlOpType.DIV,

    HwtOps.ULE: HdlOpType.LE,
    HwtOps.ULT: HdlOpType.LT,
    HwtOps.UGT: HdlOpType.GT,
    HwtOps.UGE: HdlOpType.GE,

    HwtOps.SLE: HdlOpType.LE,
    HwtOps.SLT: HdlOpType.LT,
    HwtOps.SGT: HdlOpType.GT,
    HwtOps.SGE: HdlOpType.GE,

    HwtOps.NOT: HdlOpType.NEG,
    HwtOps.MINUS_UNARY: HdlOpType.MINUS_UNARY,
    HwtOps.RISING_EDGE: HdlOpType.RISING,
    HwtOps.FALLING_EDGE: HdlOpType.FALLING,
    HwtOps.CALL: HdlOpType.CALL,
    HwtOps.DOT: HdlOpType.DOT,
}
