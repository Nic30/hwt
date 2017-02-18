from hwt.synthesizer.interfaceLevel.interfaceUtils.utils import walkPhysInterfaces


def defaultUnitName(unit, sugestedName=None):
    if not sugestedName:
        defNameFn = None
        try:
            defNameFn = unit._getDefaultName
        except AttributeError:
            pass
        
        if defNameFn:
            return defNameFn()
            
        return unit.__class__.__name__
    else:
        return sugestedName

def walkSignalOnUnit(unit):
    for i in unit._interfaces:
        yield from walkPhysInterfaces(i)
