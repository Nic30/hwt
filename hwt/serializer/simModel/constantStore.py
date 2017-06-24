
class ConstantStore(object):
    """
    Container of constants for serializer
    """

    def __init__(self, nameCheckFn):
        self.nameCheckFn = nameCheckFn

        # {value:usedName}
        self._cache = {}

    def getConstName(self, val):
        try:
            return self._cache[val]
        except KeyError:
            c = self.nameCheckFn("const_", val)
            self._cache[val] = c
            return c
