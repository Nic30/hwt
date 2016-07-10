from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.function import Function
from hdl_toolkit.hdlObjects.types.defs import INT

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
        
        if operator.operator in (AllOps.RISING_EDGE, AllOps.EVENT):
            ops.append(simulator.env.now)
        
        return self._evalFn(*ops)

    def __repr__(self):
        return "<OpDefinition %s>" % (self.id)
            
class AllOps():
    _idsInited = False
    """
    @attention: Remember that and operator "and" is & and "or" is |, "and" and "or" can not be used because
    they can not be overloaded
    @attention: These are operators of internal AST, the are not equal to verilog or vhdl operators
    """
    
    NOT = OpDefinition(lambda a :~a)
    EVENT = OpDefinition(lambda a, now: a._hasEvent(now))
    RISING_EDGE = OpDefinition(lambda a , now: a._onRisingEdge(now))  # unnecessary
    DIV = OpDefinition(lambda a, b : a // b)
    ADD = OpDefinition(lambda a, b : a + b)
    SUB = OpDefinition(lambda a, b : a - b)
    POW = OpDefinition(lambda a, b : a ** b)
    UN_MINUS = OpDefinition(lambda a :-a)
    MOD = OpDefinition(lambda a, b : a % b)
    MUL = OpDefinition(lambda a, b : a * b)
    NEQ = OpDefinition(lambda a, b : a != b)
    XOR = OpDefinition(lambda a, b : a != b)
    EQ = OpDefinition(lambda a, b : a._eq(b))
    DOT = OpDefinition(lambda a, name : getattr(a, name))

    AND_LOG = OpDefinition(lambda a, b : a & b)
    OR_LOG = OpDefinition(lambda a, b : a | b)

    DOWNTO = OpDefinition(lambda a, b : a._downto(b))
    
    GREATERTHAN = OpDefinition(lambda a, b : a > b)
    GE = OpDefinition(lambda a, b : a >= b)
    LOWERTHAN = OpDefinition(lambda a, b : a < b)
    LE = OpDefinition(lambda a, b : a <= b)
    
    CONCAT = OpDefinition(lambda a, b : a._concat(b))

    INDEX = OpDefinition(lambda a, b : a[b])
    
    TERNARY = OpDefinition(lambda a, b, c : a._ternary(b, c))
    
    CALL = OpDefinition(lambda a, *ops: a.call(*ops))
    
    BitsToInt = OpDefinition(lambda a : a._convert(INT))
    IntToBits = OpDefinition(lambda a : a._convert())
    
    BitsAsSigned = OpDefinition(lambda a : a._signed())
    BitsAsUnsigned = OpDefinition(lambda a : a._unsigned())
    BitsAsVec = OpDefinition(lambda a : a._vec())
    
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
