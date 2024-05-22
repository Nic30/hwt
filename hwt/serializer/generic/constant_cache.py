from hwt.hdl.const import HConst
from hwt.serializer.generic.tmpVarConstructor import TmpVarConstructor
from hwt.mainBases import RtlSignalBase


class ConstantCache(object):
    """
    Container of constants for serializer.
    Used to extract constants as constant variables.
    """

    def __init__(self, toHdlAst, tmpVars: TmpVarConstructor):
        self.tmpVars = tmpVars
        self.toHdlAst = toHdlAst

        # {value:usedName}
        self._cache = {}

    def extract_const_val_as_const_var(self, val: HConst) -> RtlSignalBase:
        """
        Create a constant variable with a value specified
        or use existing variable with same value
        """
        try:
            return self._cache[val]
        except KeyError:
            if isinstance(val.val, int):
                if val.val < 0:
                    name = "const_m%d_" % -val.val
                else:
                    name = f"const_{val.val:d}_"
            else:
                name = "const_"

            toHdlAst = self.toHdlAst
            cc = toHdlAst.constCache
            try:
                # dissable const cache as the value is beeing extracted
                # and we want to prevent recursion
                toHdlAst.constCache = None
                c = self.tmpVars.create_var(name, val._dtype, def_val=val, const=True)
            finally:
                toHdlAst.constCache = cc

            self._cache[val] = c
            return c
