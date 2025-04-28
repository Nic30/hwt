from operator import floordiv, add, sub, inv, mul, ne, and_, or_, \
    xor, gt, ge, lt, le, getitem, neg
from typing import Optional

from hdlConvertorAst.hdlAst._expr import HdlOpType
from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.types.defs import INT, SLICE


def _getVal(v):
    while not isinstance(v, HConst):
        v = v._val

    return v


class HOperatorDef():
    """
    Operator definition

    :ivar ~.id: name of operator
    :ivar ~._evalFn: function which evaluates operands
    :ivar ~.hdlConvertoAstOp: an operator which is used for export to hdlConvertoAst library
    """

    def __init__(self, evalFn, allowsAssignTo=False, idStr:Optional[str]=None, hdlConvertoAstOp: Optional[HdlOpType]=None):
        self.id = idStr  # assigned automatically in HwtOps
        self._evalFn = evalFn
        self.allowsAssignTo = allowsAssignTo
        self.hdlConvertoAstOp = hdlConvertoAstOp

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    @internal
    def __hash__(self):
        return hash(self.id)

    def eval(self, operator, simulator=None):
        """Load all operands and process them by self._evalFn"""
        operands = [_getVal(o) for o in operator.operands]

        return self._evalFn(*operands)

    def __repr__(self):
        return f"<{self.__class__.__name__:s} {self.id:s}>"


def isEventDependentOp(operator):
    return operator in (HwtOps.RISING_EDGE, HwtOps.FALLING_EDGE)


def onRisingEdgeFn(a):
    return a._onRisingEdge()


def onFallingEdgeFn(a):
    return a._onFallingEdge()


def dotOpFn(a, name):
    return getattr(a, name)


# [TODO] downto / to are relict of vhdl and should be replaced with slice
def downtoFn(a: int, b: int):
    return SLICE.from_py(slice(a, b, -1))


def toFn(a: int, b: int):
    return SLICE.from_py(slice(a, b, 1))


def concatFn(a: "AnyHBitsValue", b: "AnyHBitsValue") -> "AnyHBitsValue":
    return a._concat(b)


def power(base, exp):
    return base ** exp


def eqFn(a, b):
    return a._eq(b)


def ternaryFn(cond: "AnyHBitsValue", vTrue, vFalse):
    return cond._ternary(vTrue, vFalse)


def callFn(fn: "HdlFunctionDef", *operands, **kwargs):
    return fn(*operands, **kwargs)


def bitsToIntFn(a: "AnyHBitsValue"):
    return a._auto_cast(INT)


def intToBitsFn(a: "AnyHBitsValue", t: "HdlType"):
    return a._auto_cast(t)


def bitsAsSignedFn(a: "AnyHBitsValue"):
    return a._signed()


def bitsAsUnsignedFn(a: "AnyHBitsValue"):
    return a._unsigned()


def bitsAsVec(a: "AnyHBitsValue"):
    return a._vec()


def zextFn(a: "AnyHBitsValue", newWidth: int):
    return a._zext(newWidth)


def sextFn(a: "AnyHBitsValue", newWidth: int):
    return a._sext(newWidth)


def truncFn(a: "AnyHBitsValue", newWidth: int):
    return a._trunc(newWidth)


class HwtOps():
    """
    :attention: Remember that and operator "and" is & and "or" is \\|, "and"
        and "or" can not be used because they can not be overloaded
    :attention: These are operators of internal AST,
        they are not equal to verilog or vhdl operators
    """
    RISING_EDGE = HOperatorDef(onRisingEdgeFn)  # unnecessary
    FALLING_EDGE = HOperatorDef(onFallingEdgeFn)  # unnecessary

    MINUS_UNARY = HOperatorDef(neg)
    DIV = HOperatorDef(floordiv)
    UDIV = HOperatorDef(lambda a, b: a._unsigned() // b._unsigned())
    SDIV = HOperatorDef(lambda a, b: a._signed() // b._signed())

    ADD = HOperatorDef(add)
    SUB = HOperatorDef(sub)
    POW = HOperatorDef(power)
    UREM = HOperatorDef(lambda a, b: a._unsigned() % b._unsigned())
    SREM = HOperatorDef(lambda a, b: a._signed() % b._signed())
    # MUL bit_length and sign of src0, src1 and dst is the same
    # sign/unsign variant with double result width is recognized from sext/zext of operands in final phases of serialization 
    MUL = HOperatorDef(mul)

    NOT = HOperatorDef(inv, allowsAssignTo=True)
    XOR = HOperatorDef(xor)
    AND = HOperatorDef(and_)
    OR = HOperatorDef(or_)

    DOT = HOperatorDef(dotOpFn, allowsAssignTo=True)
    DOWNTO = HOperatorDef(downtoFn)
    TO = HOperatorDef(toFn)
    CONCAT = HOperatorDef(concatFn, allowsAssignTo=True)
    # :note: SEXT, ZEXT, TRUNC are redundant as it can be implemented using INDEX/CONCAT however they exist
    #        from performance reasons as patern match for them would be very common during optimizations and
    #        specific evaluation functions may be significantly faster
    # :note: normalization rules:
    #    * SEXT, ZEXT is prefered over concatenation
    #    * sext(a:1b) should be used internally instead of concat(a, a)
    #    * TRUNC is prefered over index with a single exception
    #      * x[0] should be used internally instead of trunc(x, 1)
    SEXT = HOperatorDef(sextFn)  # sign extension of bit vector to larger width
    ZEXT = HOperatorDef(zextFn)  # zero extension  of bit vector to larger width
    TRUNC = HOperatorDef(truncFn, allowsAssignTo=True)  # truncate width of bit vector

    EQ = HOperatorDef(eqFn)
    NE = HOperatorDef(ne)
    # :note: for compare operands without U/S the info about sign is stored in type of operands
    #     for U/S variant the signed flag in the type is ignored and signines is forced by operator definition 
    GT = HOperatorDef(gt)
    GE = HOperatorDef(ge)
    LT = HOperatorDef(lt)
    LE = HOperatorDef(le)

    ULE = HOperatorDef(lambda a, b: a._unsigned() <= b._unsigned())
    ULT = HOperatorDef(lambda a, b: a._unsigned() < b._unsigned())
    UGT = HOperatorDef(lambda a, b: a._unsigned() > b._unsigned())
    UGE = HOperatorDef(lambda a, b: a._unsigned() >= b._unsigned())

    SLE = HOperatorDef(lambda a, b: a._signed() <= b._signed())
    SLT = HOperatorDef(lambda a, b: a._signed() < b._signed())
    SGT = HOperatorDef(lambda a, b: a._signed() > b._signed())
    SGE = HOperatorDef(lambda a, b: a._signed() >= b._signed())
    
    # :note: INDEX is used for arrays and also for bit vectors
    INDEX = HOperatorDef(getitem, allowsAssignTo=True)
    TERNARY = HOperatorDef(ternaryFn)
    CALL = HOperatorDef(callFn)

    BitsAsSigned = HOperatorDef(bitsAsSignedFn, allowsAssignTo=True)
    BitsAsUnsigned = HOperatorDef(bitsAsUnsignedFn, allowsAssignTo=True)
    BitsAsVec = HOperatorDef(bitsAsVec, allowsAssignTo=True)


for a_name in dir(HwtOps):
    o = getattr(HwtOps, a_name)
    if isinstance(o, HOperatorDef):
        o.id = a_name

CAST_OPS = (HwtOps.BitsAsVec, HwtOps.BitsAsSigned, HwtOps.BitsAsUnsigned)
BITWISE_OPS = (HwtOps.NOT, HwtOps.XOR, HwtOps.AND, HwtOps.OR)
COMPARE_OPS = (
    HwtOps.EQ,
    HwtOps.NE,
    HwtOps.GT,
    HwtOps.GE,
    HwtOps.LT,
    HwtOps.LE,
    HwtOps.ULE,
    HwtOps.ULT,
    HwtOps.UGT,
    HwtOps.UGE,
    HwtOps.SLE,
    HwtOps.SLT,
    HwtOps.SGT,
    HwtOps.SGE,
)

# change of compare operator on operand order swap
CMP_OP_SWAP = {
    HwtOps.EQ: HwtOps.EQ,  # (a == b) == (b == a)
    HwtOps.NE: HwtOps.NE,  # (a != b) == (b != a)

    HwtOps.GT: HwtOps.LT,  # (a > b)  == (b < a)
    HwtOps.GE: HwtOps.LE,  # (a >= b) == (b <= a)
    HwtOps.LT: HwtOps.GT,  # (a < b)  == (b > a)
    HwtOps.LE: HwtOps.GE,  # (a <= b) == (b >= a)

    HwtOps.UGT: HwtOps.ULT,
    HwtOps.UGE: HwtOps.ULE,
    HwtOps.ULT: HwtOps.UGT,
    HwtOps.ULE: HwtOps.UGE,

    HwtOps.SGT: HwtOps.SLT,
    HwtOps.SGE: HwtOps.SLE,
    HwtOps.SLT: HwtOps.SGT,
    HwtOps.SLE: HwtOps.SGE,

}

CMP_OPS_NEG = {
    HwtOps.EQ: HwtOps.NE,
    HwtOps.NE: HwtOps.EQ,

    HwtOps.GT: HwtOps.LE,
    HwtOps.GE: HwtOps.LT,
    HwtOps.LT: HwtOps.GE,
    HwtOps.LE: HwtOps.GT,

    HwtOps.UGT: HwtOps.ULE,
    HwtOps.UGE: HwtOps.ULT,
    HwtOps.ULT: HwtOps.UGE,
    HwtOps.ULE: HwtOps.UGT,

    HwtOps.SGT: HwtOps.SLE,
    HwtOps.SGE: HwtOps.SLT,
    HwtOps.SLT: HwtOps.SGE,
    HwtOps.SLE: HwtOps.SGT,
}

# always commutative operators for which order of operands does not matter
ALWAYS_COMMUTATIVE_OPS = (HwtOps.EQ, HwtOps.NE, HwtOps.XOR, HwtOps.AND, HwtOps.OR, HwtOps.ADD, HwtOps.MUL)
# always commutative associative operators for which order of operands in expression tree does not matter
ALWAYS_ASSOCIATIVE_COMMUTATIVE_OPS = (HwtOps.XOR, HwtOps.AND, HwtOps.OR, HwtOps.ADD, HwtOps.MUL)
EVENT_OPS = (HwtOps.RISING_EDGE, HwtOps.FALLING_EDGE)
