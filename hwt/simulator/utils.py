import sys

from hwt.serializer.generic.indent import getIndent
from hwt.synthesizer.hObjList import HObjList
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase


def pprintInterface(intf, prefix="", indent=0, file=sys.stdout):
    """
    Pretty print interface
    """
    try:
        s = intf._sig
    except AttributeError:
        s = None
    if s is None:
        s = ""
    else:
        s = " " + repr(s)

    file.write("".join([getIndent(indent), prefix, repr(intf._getFullName()),
                        s]))
    file.write("\n")

    if isinstance(intf, HObjList):
        for i, p in enumerate(intf):
            # interfaces have already name of this array and index in it's name
            pprintInterface(p, prefix=prefix, indent=indent + 1, file=file)
    else:
        for i in intf._interfaces:
            pprintInterface(i, indent=indent + 1, file=file)


def pprintAgents(unitOrIntf, indent=0, prefix="", file=sys.stdout):
    if isinstance(unitOrIntf, InterfaceBase):
        ag = unitOrIntf._ag
    elif isinstance(unitOrIntf, HObjList):
        for i, item in enumerate(unitOrIntf):
            item_prefix = "%s_%d" % (prefix, i)
            pprintAgents(item, indent=indent+1, prefix=item_prefix, file=file)
        return
    else:
        ag = None

    if ag is not None:
        file.write("%s%s%r\n" % (getIndent(indent), prefix, ag))

    for i in unitOrIntf._interfaces:
        pprintAgents(i, indent + 1, file=file)
