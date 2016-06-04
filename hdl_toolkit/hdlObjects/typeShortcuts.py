from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.synthetisator.rtlLevel.signal import Signal, SignalNode
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.operator import Operator
from hdl_toolkit.hdlObjects.types.defs import INT, BOOL, STR, BIT
from hdl_toolkit.hdlObjects.types.bits import Bits

def getSignalOrValue(val, pyT, hdlT):
    if isinstance(val, Value) or isinstance(val, Signal):
        return val
    else:
        v = pyT(val)
        return hdlT.fromPy(v)

def fromPyValToValueFn(pyT, hdlT):
    def fn(val):
        """create hdl value from hdl Value or Param or python value"""
        val = getSignalOrValue(val, pyT, hdlT)
        assert(val._dtype == hdlT)
        return val
    return fn

hInt = fromPyValToValueFn(int, INT)

# create hdl boolean value (for example boolean value in vhdl)
hBool = fromPyValToValueFn(bool, BOOL)


# create hdl string value (for example string value in vhdl)
hStr = fromPyValToValueFn(str, STR)

# create hdl bit value (for example STD_LOGIC value in vhdl)
hBit = fromPyValToValueFn(int, BIT)

def mkRange(width):
    """Make hdl range (for example 1 downto 0 in vhdl)
       @return: (width -1, 0) 
    """
    to = getSignalOrValue(width, int, INT)
    if isinstance(to, Value):
        to = hInt(to) - hInt(1)
    else:
        to = to - 1
    return SignalNode.resForOp(Operator(AllOps.DOWNTO, [to, hInt(0)]))

def vecT(width, signed=None):
    """Make contrained vector type"""
    return Bits(widthConstr=mkRange(width), signed=signed, forceVector=True)

def vec(val, width):
    """create hdl vector value"""
    assert(val < 2 ** width)
    return vecT(width).fromPy(val)

def hRange(upper, lower):
    # [TODO] param conversion if necessary
    return SignalNode.resForOp(Operator(AllOps.DOWNTO, [lower, upper]))
