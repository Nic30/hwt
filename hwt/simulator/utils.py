from random import Random
import sys

from hwt.serializer.serializerClases.indent import getIndent
from hwt.synthesizer.interfaceLevel.interfaceUtils.proxy import InterfaceProxy


def valueHasChanged(valA, valB):
    return valA.val is not valB.val or valA.vldMask != valB.vldMask


def agent_randomize(agent, timeQuantum, seed):
    random = Random(seed)

    def randomEnProc(simulator):
        # small space at start to modify agents when they are inactive
        yield simulator.wait(timeQuantum / 4)
        while True:
            agent.enable = random.random() < 0.5
            delay = int(random.random() * timeQuantum)
            yield simulator.wait(delay)

    return randomEnProc


def pprintInterface(intf, prefix="", indent=0, file=sys.stdout):
    """
    Pretty print interface
    """
    try:
        s = intf._sig
    except AttributeError:
        s = ""
    if s is not "":
        s = repr(s)

    file.write("".join([getIndent(indent), prefix, repr(intf._getFullName()), " ", s]))
    file.write("\n")

    for i in intf._interfaces:
        if isinstance(intf, InterfaceProxy):
            assert isinstance(i, InterfaceProxy), (intf, i)
        pprintInterface(i, indent=indent + 1, file=file)

    if intf._arrayElemCache:
        assert len(intf) == len(intf._arrayElemCache)
        for i, p in enumerate(intf):
            pprintInterface(p, prefix="p%d:" % i, indent=indent + 1, file=file)


def _pprintAgents(intf, indent, prefix="", file=sys.stdout):
    if intf._ag is not None:
        file.write("%s%s%r\n" % (getIndent(indent), prefix, intf._ag))
    for i in intf._interfaces:
        _pprintAgents(i, indent + 1, file=file)

    if intf._arrayElemCache:
        assert len(intf) == len(intf._arrayElemCache)
        for i, p in enumerate(intf):
            _pprintAgents(p, indent + 1, prefix="p%d:" % i, file=file)


def pprintAgents(unitOrIntf, indent=0, file=sys.stdout):
    """
    Pretty print agents
    """
    prefix = unitOrIntf._name + ":"
    for intf in unitOrIntf._interfaces:
        _pprintAgents(intf, indent, prefix, file=file)
