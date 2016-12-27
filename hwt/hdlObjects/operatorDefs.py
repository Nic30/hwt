from hwt.hdlObjects.value import Value
from hwt.hdlObjects.function import Function
from hwt.hdlObjects.types.defs import INT
from operator import floordiv, add, sub, inv, mod, mul, ne, and_, or_, \
    xor, gt, ge, lt, le, getitem
from hwt.hdlObjects.constants import SENSITIVITY

class OpDefinition():
    """
    OperatorDefinition
    @ivar id: name of operator
    @ivar _evalFn: function which evaluates operands
    """
    def __init__(self, evalFn):
        self.id = None  # assigned automatically in AllOps  
        self._evalFn = evalFn
        
    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id
    
    def  __hash__(self):
        return hash(self.id)
    
    def eval(self, operator, simulator=None):
        """Load all operands and process them by self._evalFn"""
        def getVal(v):
            while not isinstance(v, (Value, Function)):
                v = v._val
            
            return v

        ops = list(map(getVal, operator.ops))
        
        if isEventDependentOp(operator.operator):
            ops.append(simulator.now)
        elif operator.operator == AllOps.IntToBits:
            ops.append(operator.result._dtype)
        
        return self._evalFn(*ops)

    def __repr__(self):
        return "<OpDefinition %s>" % (self.id)

def isEventDependentOp(operator):
    return operator in (AllOps.RISING_EDGE, AllOps.EVENT, AllOps.FALLIGN_EDGE)


def eventFn(a, now):
    return a._hasEvent(now)

def onRisingEdgeFn(a, now):
    return a._onRisingEdge(now)

def onFallingEdge(a, now):
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

def callFn(fn, *ops):
    return a.call(*ops)

def bitsToIntFn(a):
    return a._convert(INT)

def intToBitsFn(a, t):
    return  a._convert(t)

def bitsAsSignedFn(a):
    return a._signed()

def bitsAsUnsignedFn(a):
    return a._unsigned()

def bitsAsVec(a):
    return a._vec()

class AllOps():
    _idsInited = False
    """
    @attention: Remember that and operator "and" is & and "or" is |, "and" and "or" can not be used because
    they can not be overloaded
    @attention: These are operators of internal AST, the are not equal to verilog or vhdl operators
    """
    
    
    EVENT = OpDefinition(eventFn)
    RISING_EDGE = OpDefinition(onRisingEdgeFn)  # unnecessary
    FALLIGN_EDGE = OpDefinition(onFallingEdge)  # unnecessary
    
    DIV = OpDefinition(floordiv)
    ADD = OpDefinition(add)
    SUB = OpDefinition(sub)
    POW = OpDefinition(power)
    UN_MINUS = OpDefinition(inv)
    MOD = OpDefinition(mod)
    MUL = OpDefinition(mul)
    
    NOT = OpDefinition(inv)
    XOR = OpDefinition(xor)
    AND_LOG = OpDefinition(and_)
    OR_LOG = OpDefinition(or_)

    DOT = OpDefinition(dotOpFn)
    DOWNTO = OpDefinition(downtoFn)
    TO = OpDefinition(toFn)
    CONCAT = OpDefinition(concatFn)
    
    EQ = OpDefinition(eqFn)
    NEQ = OpDefinition(ne)
    GREATERTHAN = OpDefinition(gt)
    GE = OpDefinition(ge)
    LOWERTHAN = OpDefinition(lt)
    LE = OpDefinition(le)
    

    INDEX = OpDefinition(getitem)
    TERNARY = OpDefinition(ternaryFn)
    CALL = OpDefinition(callFn)
    
    BitsToInt = OpDefinition(bitsToIntFn)
    IntToBits = OpDefinition(intToBitsFn)
    
    BitsAsSigned = OpDefinition(bitsAsSignedFn)
    BitsAsUnsigned = OpDefinition(bitsAsUnsignedFn)
    BitsAsVec = OpDefinition(bitsAsVec)
    
    allOps = {}
        
    @classmethod
    def opByName(cls, name):
        return getattr(cls, name)
    
if not AllOps._idsInited:
    for a in dir(AllOps):
        o = getattr(AllOps, a)
        if isinstance(o, OpDefinition):
            o.id = a
            
    AllOps._idsInited = True

def sensitivityByOp(op):
    if op == AllOps.RISING_EDGE:
        return SENSITIVITY.RISING
    elif op == AllOps.FALLIGN_EDGE:
        return SENSITIVITY.FALLING
    else:
        assert op == AllOps.EVENT
        return SENSITIVITY.ANY
