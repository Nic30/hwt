
from hdl_toolkit.hdlObjects.types.defs import INT, STR, BOOL
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase
from hdl_toolkit.hdlObjects.variables import SignalItem
defaultConversions = {int: INT,
                      str: STR,
                      bool: BOOL}
def toHVal(op):
    """Convert python value object to object of hdl type value"""
    if isinstance(op, Value) or isinstance(op, SignalItem):
        return op
    elif isinstance(op, InterfaceBase):
        return op._sig
    else:
        try:
            hType = defaultConversions[type(op)]
        except KeyError:
            hType = None
        
        if hType is None:
            raise TypeError("%s" % (op.__class__))
        return  hType.fromPy(op)
    
def checkOperands(ops):
    _ops = []
    for op in ops:
        _ops.append(toHVal(op))
    return _ops
