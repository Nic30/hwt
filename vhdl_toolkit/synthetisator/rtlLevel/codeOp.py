from vhdl_toolkit.templates import VHDLTemplates


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
        return VHDLTemplates.If.render(cond=self.cond.asVhdl(),
                                       ifTrue=self.ifTrue,
                                       ifFalse=self.ifFalse)
     
