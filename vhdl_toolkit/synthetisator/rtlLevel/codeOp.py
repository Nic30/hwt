from vhdl_toolkit.synthetisator.rtlLevel.signal import exp__str__, Signal
from vhdl_toolkit.templates import VHDLTemplates
from vhdl_toolkit.types import VHDLBoolean


def If(cond, ifTrue=[], ifFalse=[]):
    # only assigments are expected there    
    for stm in ifTrue:
        stm.cond.add(cond)
    for stm in ifFalse:
        stm.cond.add(cond.opNot())
    
    ret = []
    ret.extend(ifTrue)
    ret.extend(ifFalse)
    return ret


class IfContainer:
    def __init__(self, cond, ifTrue=[], ifFalse=[]):
        self.cond = cond
        self.ifTrue = ifTrue
        self.ifFalse = ifFalse
    def __str__(self):
        condResult = Signal(None, VHDLBoolean())
        return VHDLTemplates.If.render(cond=exp__str__(condResult, self.cond), ifTrue=self.ifTrue, ifFalse = self.ifFalse)
     
