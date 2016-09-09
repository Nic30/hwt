from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlMemoryBase
from hdl_toolkit.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hdl_toolkit.synthesizer.interfaceLevel.mainBases import InterfaceBase

class RtlSyncSignal(RtlMemoryBase, RtlSignal):
    """
    Syntax sugar,
    every write is made to next signal, "next" is assigned
    to main signal on every clock rising edge
    """
    
    def __init__(self, ctx, name, var_type, defaultVal=None):
        """
        @param ctx: context in which is sig. created (instance of RtlNetlist)
        @param name: suggested name
        @param var_type: type of signal
        @param defaultVal: default value for signal (used as def. val in hdl and for reset)  
        """
        super().__init__(ctx, name, var_type, defaultVal)
        self.next = RtlSignal(ctx, name + "_next", var_type)
           
    def __pow__(self, source):
        """
        assign to signal which is next value of this register
        @return: list of assignments
        """
        if isinstance(source, InterfaceBase):
            source = source._sig
        
        if source is None:
            source = self._dtype.fromPy(None)
        else:
            source = toHVal(source)
            source = source._dtype.convert(source, self._dtype)
        
        a = Assignment(source, self.next)
        a.cond = set()
        # [TODO] check no operator reverse should happen
        self.next.drivers.append(a)
        if not isinstance(source, Value):
            source.endpoints.append(a)
        return [a]
