from hdlConvertorAst.hdlAst._expr import HdlOpType
from hwt.hdl.operatorDefs import AllOps


HWT_TO_HDLCONVEROTR_OPS = {
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
    AllOps.NOT: HdlOpType.NEG,
    AllOps.MINUS_UNARY: HdlOpType.MINUS_UNARY,
    AllOps.RISING_EDGE: HdlOpType.RISING,
    AllOps.FALLING_EDGE: HdlOpType.FALLING,
}
