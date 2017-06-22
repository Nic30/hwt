from hwt.hdlObjects.typeShortcuts import vec


def fitTo(what, to):
    """
    Slice signal "what" to fit in "to"
    or
    extend "what" with zeros to same width as "to"

    little-endian impl.
    """

    whatWidth = what._dtype.bit_length()
    toWidth = to._dtype.bit_length()
    if toWidth == whatWidth:
        return what
    elif toWidth < whatWidth:
        # slice
        return what[toWidth:]
    else:
        if what._dtype.signed:
            raise NotImplementedError("Signed extension")
        # extend
        return vec(0, toWidth - whatWidth)._concat(what)
