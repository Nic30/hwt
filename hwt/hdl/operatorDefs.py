from operator import floordiv, add, sub, inv, mod, mul, ne, and_, or_, \
    xor, gt, ge, lt, le, getitem, neg

from hwt.doc_markers import internal
from hwt.hdl.types.defs import INT, SLICE
from hwt.hdl.value import HValue


def _getVal(v):
    while not isinstance(v, HValue):
        v = v._val

    return v


class OpDefinition():
    """
    Operator definition

    :ivar ~.id: name of operator
    :ivar ~._evalFn: function which evaluates operands
    """

    def __init__(self, evalFn, allowsAssignTo=False, idStr=None):
        self.id = idStr  # assigned automatically in AllOps
        self._evalFn = evalFn
        self.allowsAssignTo = allowsAssignTo

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
    return operator in (AllOps.RISING_EDGE, AllOps.FALLING_EDGE)


def onRisingEdgeFn(a):
    return a._onRisingEdge()


def onFallingEdgeFn(a):
    return a._onFallingEdge()


def dotOpFn(a, name):
    return getattr(a, name)


# [TODO] downto / to are relict of vhdl and should be replaced with slice
def downtoFn(a, b):
    return SLICE.from_py(slice(a, b, -1))


def toFn(a, b):
    return SLICE.from_py(slice(a, b, 1))


def concatFn(a, b):
    return a._concat(b)


def power(base, exp):
    return base ** exp


def eqFn(a, b):
    return a._eq(b)


def ternaryFn(a, b, c):
    return a._ternary(b, c)


def callFn(fn, *operands, **kwargs):
    return fn(*operands, **kwargs)


def bitsToIntFn(a):
    return a._auto_cast(INT)


def intToBitsFn(a, t):
    return a._auto_cast(t)


def bitsAsSignedFn(a):
    return a._signed()


def bitsAsUnsignedFn(a):
    return a._unsigned()


def bitsAsVec(a):
    return a._vec()


class AllOps():
    """
    :attention: Remember that and operator "and" is & and "or" is \|, "and"
        and "or" can not be used because they can not be overloaded
    :attention: These are operators of internal AST,
        they are not equal to verilog or vhdl operators
    """
    RISING_EDGE = OpDefinition(onRisingEdgeFn)  # unnecessary
    FALLING_EDGE = OpDefinition(onFallingEdgeFn)  # unnecessary

    MINUS_UNARY = OpDefinition(neg)
    DIV = OpDefinition(floordiv)
    UDIV = OpDefinition(lambda a, b: a._unsigned() // b._unsigned())
    SDIV = OpDefinition(lambda a, b: a._signed() <= b._signed())

    ADD = OpDefinition(add)
    SUB = OpDefinition(sub)
    POW = OpDefinition(power)
    MOD = OpDefinition(mod)
    MUL = OpDefinition(mul)

    NOT = OpDefinition(inv, allowsAssignTo=True)
    XOR = OpDefinition(xor)
    AND = OpDefinition(and_)
    OR = OpDefinition(or_)

    DOT = OpDefinition(dotOpFn)
    DOWNTO = OpDefinition(downtoFn)
    TO = OpDefinition(toFn)
    CONCAT = OpDefinition(concatFn, allowsAssignTo=True)

    EQ = OpDefinition(eqFn)
    NE = OpDefinition(ne)
    GT = OpDefinition(gt)
    GE = OpDefinition(ge)
    LT = OpDefinition(lt)
    LE = OpDefinition(le)

    ULE = OpDefinition(lambda a, b: a._unsigned() <= b._unsigned())
    ULT = OpDefinition(lambda a, b: a._unsigned() < b._unsigned())
    UGT = OpDefinition(lambda a, b: a._unsigned() > b._unsigned())
    UGE = OpDefinition(lambda a, b: a._unsigned() >= b._unsigned())

    SLE = OpDefinition(lambda a, b: a._signed() <= b._signed())
    SLT = OpDefinition(lambda a, b: a._signed() < b._signed())
    SGT = OpDefinition(lambda a, b: a._signed() > b._signed())
    SGE = OpDefinition(lambda a, b: a._signed() >= b._signed())

    INDEX = OpDefinition(getitem, allowsAssignTo=True)
    TERNARY = OpDefinition(ternaryFn)
    CALL = OpDefinition(callFn)

    BitsAsSigned = OpDefinition(bitsAsSignedFn, allowsAssignTo=True)
    BitsAsUnsigned = OpDefinition(bitsAsUnsignedFn, allowsAssignTo=True)
    BitsAsVec = OpDefinition(bitsAsVec, allowsAssignTo=True)


for a_name in dir(AllOps):
    o = getattr(AllOps, a_name)
    if isinstance(o, OpDefinition):
        o.id = a_name

CAST_OPS = (AllOps.BitsAsVec, AllOps.BitsAsSigned, AllOps.BitsAsUnsigned)
BITWISE_OPS = (AllOps.NOT, AllOps.XOR, AllOps.AND, AllOps.OR)
COMPARE_OPS = (
    AllOps.EQ,
    AllOps.NE,
    AllOps.GT,
    AllOps.GE,
    AllOps.LT,
    AllOps.LE,
    AllOps.ULE,
    AllOps.ULT,
    AllOps.UGT,
    AllOps.UGE,
    AllOps.SLE,
    AllOps.SLT,
    AllOps.SGT,
    AllOps.SGE,
)

# change of compare operator on operand order swap
CMP_OP_SWAP = {
    AllOps.EQ: AllOps.EQ,   # (a == b) == (b == a) 
    AllOps.NE: AllOps.NE,   # (a != b) == (b != a) 
    
    AllOps.GT: AllOps.LT,   # (a > b)  == (b < a) 
    AllOps.GE: AllOps.LE,   # (a >= b) == (b <= a)
    AllOps.LT: AllOps.GT,   # (a < b)  == (b > a)
    AllOps.LE: AllOps.GE,   # (a <= b) == (b >= a)

    AllOps.UGT: AllOps.ULT,
    AllOps.UGE: AllOps.ULE,
    AllOps.ULT: AllOps.UGT,
    AllOps.ULE: AllOps.UGE,

    AllOps.SGT: AllOps.SLT,
    AllOps.SGE: AllOps.SLE,
    AllOps.SLT: AllOps.SGT,
    AllOps.SLE: AllOps.SGE,

}

CMP_OPS_NEG = {
    AllOps.EQ: AllOps.NE,
    AllOps.NE: AllOps.EQ,

    AllOps.GT: AllOps.LE,
    AllOps.GE: AllOps.LT,
    AllOps.LT: AllOps.GE,
    AllOps.LE: AllOps.GT,

    AllOps.UGT: AllOps.ULE,
    AllOps.UGE: AllOps.ULT,
    AllOps.ULT: AllOps.UGE,
    AllOps.ULE: AllOps.UGT,

    AllOps.SGT: AllOps.SLE,
    AllOps.SGE: AllOps.SLT,
    AllOps.SLT: AllOps.SGE,
    AllOps.SLE: AllOps.SGT,

}

# always commutative operators for which order of operands does not matter
ALWAYS_COMMUTATIVE_OPS = (AllOps.EQ, AllOps.NE, AllOps.XOR, AllOps.AND, AllOps.OR, AllOps.ADD, AllOps.MUL)
# always commutative associative operators for which order of operands in expression tree does not matter
ALWAYS_ASSOCIATIVE_COMMUTATIVE_OPS = (AllOps.XOR, AllOps.AND, AllOps.OR, AllOps.ADD, AllOps.MUL)
EVENT_OPS = (AllOps.RISING_EDGE, AllOps.FALLING_EDGE)
