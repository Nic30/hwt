import math
from vhdl_toolkit.synthetisator.param import getParam
from vhdl_toolkit.hdlObjects.specialValues import Unconstrained
from vhdl_toolkit.hdlObjects.operators import Op





def expr_debug(expr):
    from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
    from vhdl_toolkit.hdlObjects.assigment import Assignment
    from vhdl_toolkit.hdlObjects.value import Value
    from vhdl_toolkit.synthetisator.rtlLevel.signal import walkAllRelatedSignals
    for s in  walkAllRelatedSignals(expr):
        print(s.__str__(declaration=True))
    def dumpSignalDrivers(sig):
        for d in sig.drivers:
            if isinstance(d, Op):
                print(Assignment(d, sig))
                for op in d.ops:
                    if isinstance(op, Value):
                        continue
                    dumpSignalDrivers(op)
            else:
                assert(isinstance(d, Assignment))
                print(d)
    
    if isinstance(expr, Signal):
        print(expr.__str__(declaration=True))
        dumpSignalDrivers(expr)
    elif isinstance(expr, Op):
        expr_debug(expr.result)
    else:
        print(expr)


def expr__str__(dst, src):
    from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
    from vhdl_toolkit.hdlObjects.operators import Op
    if isinstance(src, Op):
        return str(src)
    elif isinstance(src, Signal) and hasattr(src, 'origin'):
        return expr__str__(dst, src.origin)  # consume signal between operators
    else:
        return value2vhdlformat(dst, src)

def value2vhdlformat(dst, val):
    """ @param dst: is VHDLvariable connected with value """
    if isinstance(val, Op):
        # [TODO] type conversion
        return val
        
    elif hasattr(val, 'name') and not dst.defaultVal == val:
        return val.name
    w = dst.var_type.getWidth()
    if w == 1:
        return "'%d'" % (int(getParam(val)))
    elif w == int:
        return "%d" % getParam(val.get())
    elif w == Unconstrained:
        v = getParam(val)
        if hasattr(w, "derivedWidth"):
            bits = w.derivedWidth
        else:
            bits = v.bit_length() 
        return ('X"%0' + str(math.ceil(bits / 4)) + 'x"') % (getParam(val))
    elif w == str:
        return '"%s"' % (getParam(val))
    elif w == bool:
        return str(bool(getParam(val)))
    elif w > 1:
        return "STD_LOGIC_VECTOR(TO_UNSIGNED(%d, %s'LENGTH))" % (int(val), dst.name)
    else:
        raise Exception("value2vhdlformat can not resolve type conversion") 

class Map():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def __str__(self):
        return "%s => %s" % (self.dst.name, self.src.name)  

 
