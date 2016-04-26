from vhdl_toolkit.synthetisator.interfaceLevel.interface.utils import walkPhysInterfaces

def defaultUnitName(unit, sugestedName=None):
    if not sugestedName:
        return unit.__class__.__name__
    else:
        return sugestedName

def synthesised(u):
    for _ in u._toRtl():
        pass
    return u

def walkSignalOnUnit(unit):
    for i in unit._interfaces:
        yield from walkPhysInterfaces(i)