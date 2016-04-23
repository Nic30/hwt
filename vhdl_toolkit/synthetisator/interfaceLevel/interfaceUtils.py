from vhdl_toolkit.synthetisator.param import Param, getParam

def sameIntfAs(intf):
    _intf = intf.__class__()
    for p in intf._params:
        _intf._replaceParam(p._name, Param(getParam(p)))
    return _intf    

def connect(driver, *endpoints):
    """connect interfaces on interface level"""
    assert(driver._isAccessible)
    for ep in endpoints:
        ep._setSrc(driver)


def walkPhysInterfaces(intf):
    if intf._interfaces:
        for si in intf._interfaces:
            yield from walkPhysInterfaces(si)
    else:
        yield intf

def convert(intf, intfCls, paramsLikeIntf):
    i = intfCls()
    for p in paramsLikeIntf._params:
        raise NotImplementedError()
    i._loadDeclarations()
    
    #for i in 
    
    return i
    
    raise NotImplementedError()


def forAllParams(intf, discovered=None):
    if discovered is None:
        discovered = set()
    
    for si in intf._interfaces:
        yield from forAllParams(si, discovered)
        
    for p in intf._params:
        if p not in discovered:
            discovered.add(p)
            yield p 
