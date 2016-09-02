
class HdlRef():
    """
    hdl reference container
    """
    def __init__(self, names, caseSensitive, allChilds=False):
        self.names = HdlRef._caseSensitivityForNames(caseSensitive, names)
        self.all = allChilds

    @staticmethod
    def _caseSensitivityForNames(caseSensitive, names):
        if caseSensitive:
            return names
        else:
            return tuple([n.lower() for n in names])

    def __str__(self):
        SEPARATOR = '.'
        s = SEPARATOR.join(self.names)
        if self.all:
            s += SEPARATOR + "all"
        return s

    def __repr__(self):
        return "<HdlRef  " + str(self) + ">"
