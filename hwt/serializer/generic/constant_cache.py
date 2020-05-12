from typing import Callable

from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class ConstantCache(object):
    """
    Container of constants for serializer.
    Used to extract constants as constant variables.
    """

    def __init__(self, create_tmp_var_fn: Callable[[str, object], RtlSignalBase]):
        self.create_tmp_var_fn = create_tmp_var_fn

        # {value:usedName}
        self._cache = {}

    def extract_const_val_as_const_var(self, val):
        """
        Create a constant variable with a value specified
        or use existitng variable with same value
        """
        try:
            return self._cache[val]
        except KeyError:
            if isinstance(val.val, int):
                if val.val < 0:
                    name = "const_m%d_" % -val.val
                else:
                    name = "const_%d_" % val.val
            else:
                name = "const_"

            c = self.create_tmp_var_fn(name, val._dtype, def_val=val, const=True)
            c.const = True
            self._cache[val] = c
            return c
