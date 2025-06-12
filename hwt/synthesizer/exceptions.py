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

    def __init__(self, dst: "HwIOBase", src: "HwIOBase", exclude: Set["HwIOBase"]):
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
        srcHwIos = getattr(src, "_hwIOs", None)
        if srcHwIos is None:
            # src is likely a constant
            try:
                for f in src._dtype.fields:
                    io2 = getattr(dst, f.name, None)
                    if io2 is None and (not exclude or io2 not in exclude):
                        missing_on_dst.append(f.name)
            except AttributeError:
                # the type of src is unexpected, can not produce any good err msg.
                pass
        else:
            for sHwIO in srcHwIos:
                io2 = getattr(dst, sHwIO._name, None)
                if io2 is None and (not exclude or sHwIO not in exclude):
                    missing_on_dst.append(sHwIO._name)

        for sHwIO in dst._hwIOs:
            io2 = getattr(src, sHwIO._name, None)
            if io2 is None and (not exclude or sHwIO not in exclude):
                missing_on_src.append(sHwIO._name)

        buff = [f"<{self.__class__.__name__} {dst} <= {src}"]
        if missing_on_dst:
            buff.append(f", missing on dst: {missing_on_dst}")
        if missing_on_src:
            buff.append(f", missing on src: {missing_on_src}")
        buff.append(">")
        return "".join(buff)

    def __copy__(self):
        return self.__class__(self.dst, self.src, self.exclude)
