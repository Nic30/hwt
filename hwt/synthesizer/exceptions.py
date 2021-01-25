from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from typing import Set


class TypeConversionErr(TypeError):
    pass


class ConfErr(Exception):
    pass


class IntfLvlConfErr(ConfErr):
    """
    Interface level synthesizer user configuration error
    """
    pass


class SigLvlConfErr(ConfErr):
    """
    Signal level synthesizer user configuration error
    """
    pass


class InterfaceStructureErr(IntfLvlConfErr):
    """
    An exception which means that the two interfaces have non compatible sub-interfaces.
    (E.g. they do have a differently named signals)

    :ivar exclude: a set of sub-interfaces which should be excluded during the comparison
    """

    def __init__(self, dst: InterfaceBase, src: InterfaceBase, exclude: Set[InterfaceBase]):
        super(InterfaceStructureErr, self).__init__()
        self.src = src
        self.dst = dst
        self.exclude = exclude

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        missing_on_src = []
        missing_on_dst = []
        dst = self.dst
        src = self.src
        exclude = self.exclude
        for i in src._interfaces:
            i2 = getattr(dst, i._name, None)
            if i2 is None and (not exclude or i not in exclude):
                missing_on_dst.append(i._name)

        for i in dst._interfaces:
            i2 = getattr(src, i._name, None)
            if i2 is None and (not exclude or i not in exclude):
                missing_on_src.append(i._name)

        buff = [f"<{self.__class__.__name__} {dst} <= {src}"]
        if missing_on_dst:
            buff.append(f", missing on dst: {missing_on_dst}")
        if missing_on_src:
            buff.append(f", missing on src: {missing_on_src}")
        buff.append(">")
        return "".join(buff)

    def __copy__(self):
        return self.__class__(self.dst, self.src, self.exclude)
