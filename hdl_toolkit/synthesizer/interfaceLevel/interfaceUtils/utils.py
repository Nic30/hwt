from hdl_toolkit.synthesizer.param import Param, getParam

def sameIntfAs(intf):
    _intf = intf.__class__()
    for p in intf._params:
        _intf._replaceParam(p._name, Param(getParam(p)))
    return _intf    

def walkPhysInterfaces(intf):
    if intf._interfaces:
        for si in intf._interfaces:
            yield from walkPhysInterfaces(si)
    else:
        yield intf


def forAllParams(intf, discovered=None):
    if discovered is None:
        discovered = set()
    
    for si in intf._interfaces:
        yield from forAllParams(si, discovered)
        
    for p in intf._params:
        if p not in discovered:
            discovered.add(p)
            yield p 
