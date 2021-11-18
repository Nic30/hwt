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

    def __init__(self, evalFn, allowsAssignTo=False):
        self.id = None  # assigned automatically in AllOps
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
