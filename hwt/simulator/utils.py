import sys

from hwt.serializer.serializerClases.indent import getIndent
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase


def valueHasChanged(valA, valB):
    return valA.val is not valB.val or valA.vldMask != valB.vldMask


def pprintInterface(intf, prefix="", indent=0, file=sys.stdout):
    """
    Pretty print interface
    """
    try:
        s = intf._sig
    except AttributeError:
        s = ""
    if s is not "":
        s = " " + repr(s)

    file.write("".join([getIndent(indent), prefix, repr(intf._getFullName()),
                        s]))
    file.write("\n")

    for i in intf._interfaces:
        if isinstance(intf, InterfaceProxy):
            assert isinstance(i, InterfaceProxy), (intf, i)
        pprintInterface(i, indent=indent + 1, file=file)

    if intf._arrayElemCache:
        assert len(intf) == len(intf._arrayElemCache)
        for i, p in enumerate(intf):
            pprintInterface(p, prefix="p%d:" % i, indent=indent + 1, file=file)


def pprintAgents(unitOrIntf, indent=0, prefix="", file=sys.stdout):
    if isinstance(unitOrIntf, InterfaceBase):
        ag = unitOrIntf._ag
        arrayElemCache = unitOrIntf._arrayElemCache
    else:
        ag = None
        arrayElemCache = None

    if ag is not None:
        file.write("%s%s%r\n" % (getIndent(indent), prefix, ag))
    elif arrayElemCache:
        file.write("%s%s\n" %
                   (getIndent(indent), prefix + unitOrIntf._name + ":"))

    for i in unitOrIntf._interfaces:
        pprintAgents(i, indent + 1, file=file)

    if arrayElemCache:
        assert len(unitOrIntf) == len(arrayElemCache)
        for i, p in enumerate(unitOrIntf):
            pprintAgents(p, indent + 1, prefix="p%d:" % i, file=file)
