from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.hdlObjects.typeDefs import INT, BOOL, VECTOR, STR, BIT, RANGE
from vhdl_toolkit.synthetisator.param import getParam
from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal

def getSignalOrValue(val, pyT, hdlT):
    val = getParam(val)
    if isinstance(val, Value) or isinstance(val, Signal):
        return val
    else:
        v = pyT(val)
        return Value.fromPyVal(v, hdlT)

def fromPyValToValueFn(pyT, hdlT):
    def fn(val):
        """create hdl value from hdl Value or Param or python value"""
        val = getSignalOrValue(val, pyT, hdlT)
        assert(val.dtype == hdlT)
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
        to = to.opSub(hInt(1))
    return Value.fromPyVal([to, hInt(0)], RANGE)

def vecT(width):
    """Make contrained vector type"""
    return VECTOR(mkRange(width))

def vec(val, width):
    """create hdl vector value"""
    return Value.fromPyVal(val, vecT(width))
