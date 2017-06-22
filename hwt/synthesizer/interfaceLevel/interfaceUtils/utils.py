
class NotSpecified(Exception):
    """
    This error means that you need to implement this function to use this functionality

    f.e. you have to implement Simulation agent for interface when you create new one and you can not use existing
    """
    pass


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
