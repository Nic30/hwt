from hdlConvertorAst.hdlAst._expr import HdlOpType
from hwt.hdl.operatorDefs import AllOps


HWT_TO_HDLCONVERTOR_OPS = {
    **{op: getattr(HdlOpType, op.id) for op in [
        AllOps.AND,
        AllOps.OR,
        AllOps.XOR,
        AllOps.CONCAT,
        AllOps.DIV,
        AllOps.DOWNTO,
        AllOps.TO,
        AllOps.EQ,
        AllOps.GT,
        AllOps.GE,
        AllOps.LE,
        AllOps.POW,
        AllOps.LT,
        AllOps.SUB,
        AllOps.MUL,
        AllOps.NE,
        AllOps.ADD,
    ]},
    AllOps.UDIV: HdlOpType.DIV,
    AllOps.SDIV: HdlOpType.DIV,

    AllOps.ULE: HdlOpType.LE,
    AllOps.ULT: HdlOpType.LT,
    AllOps.UGT: HdlOpType.GT,
    AllOps.UGE: HdlOpType.GE,

    AllOps.SLE: HdlOpType.LE,
    AllOps.SLT: HdlOpType.LT,
    AllOps.SGT: HdlOpType.GT,
    AllOps.SGE: HdlOpType.GE,

    AllOps.NOT: HdlOpType.NEG,
    AllOps.MINUS_UNARY: HdlOpType.MINUS_UNARY,
    AllOps.RISING_EDGE: HdlOpType.RISING,
    AllOps.FALLING_EDGE: HdlOpType.FALLING,
    AllOps.CALL: HdlOpType.CALL,
    AllOps.DOT: HdlOpType.DOT,
}
