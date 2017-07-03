
class ConstCache(object):
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
            if isinstance(val.val, int):
                name = "const_%d_" % val.val
            else:
                name = "const_"

            c = self.nameCheckFn(name, val)
            self._cache[val] = c
            return c
