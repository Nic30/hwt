from hdlConvertor.hdlAst._expr import HdlBuiltinFn
from hwt.hdl.operatorDefs import AllOps


HWT_TO_HDLCONVEROTR_OPS = {
    **{op: getattr(HdlBuiltinFn, op.id) for op in [
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
        AllOps.NEQ,
        AllOps.ADD,
    ]},
    AllOps.NOT: HdlBuiltinFn.NEG,
    AllOps.MINUS_UNARY: HdlBuiltinFn.MINUS_UNARY,
    AllOps.RISING_EDGE: HdlBuiltinFn.RISING,
    AllOps.FALLING_EDGE: HdlBuiltinFn.FALLING,
}
