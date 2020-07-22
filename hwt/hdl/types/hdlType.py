from enum import Enum

from hwt.doc_markers import internal
from hwt.synthesizer.exceptions import TypeConversionErr


class MethodNotOverloaded(NotImplementedError):
    pass


@internal
def default_reinterpret_cast_fn(typeFrom, sigOrVal, toType):
    raise TypeConversionErr(
        "Reinterpretation of %r of type \n%r to type %r is not implemented",
        (sigOrVal, typeFrom, toType))


@internal
def default_auto_cast_fn(typeFrom, sigOrVal, toType):
    raise TypeConversionErr(
        "Conversion of %r of type \n%r to type %r is not implemented",
        (sigOrVal, typeFrom, toType))


class HdlType():
    """
    Base class for all hardware related types.

    :ivar ~._auto_cast_fn: convert function (attribute set on first convert
        function call)
    :ivar ~._reinterpret_cast_fn: reinterpret function (attribute set
        on first convert function call)
    """

    def __init__(self, const=False):
        self.const = const
    
    def _from_py(self, v, vld_mask):
        """
        same as from_py just without type checks
        """
        return self.getValueCls()._from_py(self, v, vld_mask)
    
    def from_py(self, v, vld_mask=None):
        """
        Construct value of this type.
        Delegated on value class for this type
        """
        if isinstance(v, Enum):
            v = v.value
        return self.getValueCls().from_py(self, v, vld_mask=vld_mask)

    def auto_cast(self, sigOrVal, toType):
        """
        Cast value or signal of this type to another compatible type.

        :param sigOrVal: instance of signal or value to cast
        :param toType: instance of HdlType to cast into
        """
        if sigOrVal._dtype == toType:
            return sigOrVal

        try:
            c = self._auto_cast_fn
        except AttributeError:
            c = self.get_auto_cast_fn()
            self._auto_cast_fn = c

        return c(self, sigOrVal, toType)

    def reinterpret_cast(self, sigOrVal, toType):
        """
        Cast value or signal of this type to another type of same size.

        :param sigOrVal: instance of signal or value to cast
        :param toType: instance of HdlType to cast into
        """
        try:
            return self.auto_cast(sigOrVal, toType)
        except TypeConversionErr:
            pass

        try:
            r = self._reinterpret_cast_fn
        except AttributeError:
            r = self.get_reinterpret_cast_fn()
            self._reinterpret_cast_fn = r

        return r(self, sigOrVal, toType)

    @internal
    @classmethod
    def get_auto_cast_fn(cls):
        """
        Get method for converting type
        """
        return default_auto_cast_fn

    @internal
    @classmethod
    def get_reinterpret_cast_fn(cls):
        """
        Get method for converting type
        """
        return default_reinterpret_cast_fn

    @internal
    @classmethod
    def getValueCls(cls):
        """
        :attention: Overrode in implementation of concrete HdlType.

        :return: class for value derived from this type
        """
        raise NotImplementedError()

    def _as_hdl(self, to_Hdl: "ToHdlAst", declaration):
        raise MethodNotOverloaded()

    def _as_hdl_requires_def(self, to_Hdl: "ToHdlAst", other_types: list):
        raise MethodNotOverloaded()

    def __getitem__(self, key):
        """
        [] operator to create an array of this type.
        """
        assert int(key) > 0, key  # array has to have some items
        from hwt.hdl.types.array import HArray
        return HArray(self, key)

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and Array)
        """
        name = getattr(self, "name", "")
        return "<%s %s>" % (self.__class__.__name__, name)
