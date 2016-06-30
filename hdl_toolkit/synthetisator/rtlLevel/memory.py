from hdl_toolkit.synthetisator.rtlLevel.signal import RtlSignal
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlMemoryBase



class RtlMemory(RtlSignal, RtlMemoryBase):
    """
    Syntax sugar,
    every write is made to next signal, "next" is assigned
    to main signal on every clock rising edge
    """
    
    def __init__(self, name, var_type, defaultVal=None):
        super().__init__(name, var_type, defaultVal)
        self.next = RtlSignal(name + "_next", var_type, defaultVal)
        
    def _assignFrom(self, source):
        source = toHVal(source)
        a = Assignment(source, self.next)
        a.cond = set()
        self.next.drivers.append(a)
        if not isinstance(source, Value):
            source.endpoints.append(a)
             
        return a
    