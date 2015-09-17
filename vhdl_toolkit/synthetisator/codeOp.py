

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
