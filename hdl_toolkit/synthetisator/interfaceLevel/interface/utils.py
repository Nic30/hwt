from hdl_toolkit.synthetisator.param import Param, getParam
from hdl_toolkit.synthetisator.exceptions import IntfLvlConfErr

def sameIntfAs(intf):
    _intf = intf.__class__()
    for p in intf._params:
        _intf._replaceParam(p._name, Param(getParam(p)))
    return _intf    

def connect(driver, *endpoints):
    """connect interfaces on interface level"""
    if not driver._isAccessible:
        reason = ""
        if not driver._isExtern:
            reason = "(brobalbly because it is not external interface)"
        raise IntfLvlConfErr("Can not use %s because it is not accessible %s" % (repr(driver), reason))
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
    
    # for i in 
    
    raise NotImplementedError()
    return i
    


def forAllParams(intf, discovered=None):
    if discovered is None:
        discovered = set()
    
    for si in intf._interfaces:
        yield from forAllParams(si, discovered)
        
    for p in intf._params:
        if p not in discovered:
            discovered.add(p)
            yield p 
