from operator import floordiv, add, sub, inv, mod, mul, ne, and_, or_, \
    xor, gt, ge, lt, le, getitem

from hwt.hdl.constants import SENSITIVITY
from hwt.hdl.types.defs import INT
from hwt.hdl.value import Value
from _operator import neg


class OpDefinition():
    """
    Operator definition

    :ivar id: name of operator
    :ivar _evalFn: function which evaluates operands
    """
    def __init__(self, evalFn):
        self.id = None  # assigned automatically in AllOps
        self._evalFn = evalFn

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def eval(self, operator, simulator=None):
        """Load all operands and process them by self._evalFn"""
        def getVal(v):
            while not isinstance(v, Value):
                v = v._val

            return v

        operands = list(map(getVal, operator.operands))

        if isEventDependentOp(operator.operator):
            operands.append(simulator.now)
        elif operator.operator == AllOps.IntToBits:
            operands.append(operator.result._dtype)

        return self._evalFn(*operands)

    def __repr__(self):
        return "<OpDefinition %s>" % (self.id)


def isEventDependentOp(operator):
    return operator in (AllOps.RISING_EDGE, AllOps.FALLIGN_EDGE)


def onRisingEdgeFn(a, now):
    return a._onRisingEdge(now)


def onFallingEdgeFn(a, now):
    return a._onFallingEdge(now)


def dotOpFn(a, name):
    return getattr(a, name)


# [TODO] downto / to are relict of vhdl and should be replaced with slice
def downtoFn(a, b):
    return a._downto(b)


def toFn(a, b):
    return a._to(b)


def concatFn(a, b):
    return a._concat(b)


def power(base, exp):
    return base._pow(exp)


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
    :attention: Remember that and operator "and" is & and "or" is \|, "and" and "or" can not be used because
        they can not be overloaded
    :attention: These are operators of internal AST, the are not equal to verilog or vhdl operators
    """
    RISING_EDGE = OpDefinition(onRisingEdgeFn)  # unnecessary
    FALLIGN_EDGE = OpDefinition(onFallingEdgeFn)  # unnecessary

    NEG = OpDefinition(neg)
    DIV = OpDefinition(floordiv)
    ADD = OpDefinition(add)
    SUB = OpDefinition(sub)
    POW = OpDefinition(power)
    UN_MINUS = OpDefinition(inv)
    MOD = OpDefinition(mod)
    MUL = OpDefinition(mul)

    NOT = OpDefinition(inv)
    XOR = OpDefinition(xor)
    AND = OpDefinition(and_)
    OR = OpDefinition(or_)

    DOT = OpDefinition(dotOpFn)
    DOWNTO = OpDefinition(downtoFn)
    TO = OpDefinition(toFn)
    CONCAT = OpDefinition(concatFn)

    EQ = OpDefinition(eqFn)
    NEQ = OpDefinition(ne)
    GT = OpDefinition(gt)
    GE = OpDefinition(ge)
    LT = OpDefinition(lt)
    LE = OpDefinition(le)

    INDEX = OpDefinition(getitem)
    TERNARY = OpDefinition(ternaryFn)
    CALL = OpDefinition(callFn)

    BitsToInt = OpDefinition(bitsToIntFn)
    IntToBits = OpDefinition(intToBitsFn)

    BitsAsSigned = OpDefinition(bitsAsSignedFn)
    BitsAsUnsigned = OpDefinition(bitsAsUnsignedFn)
    BitsAsVec = OpDefinition(bitsAsVec)

for a in dir(AllOps):
    o = getattr(AllOps, a)
    if isinstance(o, OpDefinition):
        o.id = a


def sensitivityByOp(op):
    """
    get sensitivity type for operator
    """
    if op == AllOps.RISING_EDGE:
        return SENSITIVITY.RISING
    elif op == AllOps.FALLIGN_EDGE:
        return SENSITIVITY.FALLING
    else:
        raise TypeError()
