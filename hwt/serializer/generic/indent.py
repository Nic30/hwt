_indent = "    "
_indentCache = {}


def getIndent(indentNum):
    """
    Cached indent getter function
    """
    try:
        return _indentCache[indentNum]
    except KeyError:
        i = "".join([_indent for _ in range(indentNum)])
        _indentCache[indentNum] = i
        return i
