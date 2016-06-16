from hdl_toolkit.synthetisator.interfaceLevel.mainBases import InterfaceBase

def intfToSig(obj):
    if isinstance(obj, InterfaceBase):
        return obj._sig
    else:
        return obj

def If(cond, ifTrue=[], ifFalse=[]):
    """
    If statement
    """
    cond = intfToSig(cond)
    
    for stm in ifTrue:
        stm.cond.add(cond)
        
    for stm in ifFalse:
        stm.cond.add(~cond)
    
    ret = []
    ret.extend(ifTrue)
    ret.extend(ifFalse)
    return ret

def Switch(val, *cases):
    """
    Switch statement
    """
    top = None
    for c in reversed(cases):
        if top is None:
            top = c[1]
        else:
            assert(c[0] is not None)
            top = If(val._eq(c[0]),
                     c[1]
                     ,
                     top
                    )
        
    return top

