from vhdl_toolkit.hdlObjects.operator import Operator

def expr_debug(expr):
    from vhdl_toolkit.synthetisator.rtlLevel.signal import Signal
    from vhdl_toolkit.hdlObjects.assignment import Assignment
    from vhdl_toolkit.hdlObjects.value import Value
    from vhdl_toolkit.synthetisator.rtlLevel.signalWalkers import walkAllRelatedSignals
    from vhdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
  
    def dumpSignalDrivers(sig):
        for d in sig.drivers:
            if isinstance(d, Operator):
                print(Assignment(d, sig).__repr__())
                for op in d.ops:
                    if isinstance(op, Value):
                        continue
                    dumpSignalDrivers(op)
            else:
                assert(isinstance(d, Assignment))
                print(d.__repr__())
    
    for s in  walkAllRelatedSignals(expr):
        print(VhdlSerializer.SignalItem(s, declaration=True))
      
    if isinstance(expr, Signal):
        print(VhdlSerializer.SignalItem(expr))
        dumpSignalDrivers(expr)
    elif isinstance(expr, Operator):
        expr_debug(expr.result)
    else:
        print(VhdlSerializer.asHdl(expr))


class Map():
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
   
    def __str__(self):
        return "%s => %s" % (self.dst.name, self.src.name)  

 
