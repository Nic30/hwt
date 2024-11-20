from enum import Enum
from typing import Union, Type, Self

from hwt.doc_markers import internal
from hwt.synthesizer.exceptions import TypeConversionErr


class MethodNotOverloaded(NotImplementedError):
    """
    Method is missing overload of abstract parent method.
    """
    pass


class HdlType():
    """
    Base class for all hardware related types.

    :ivar ~._auto_cast_fn: convert function (attribute set on first convert
        function call)
    :ivar ~._reinterpret_cast_fn: reinterpret function (attribute set
        on first convert function call)
        
    :note: Cast functions are linked trough HldType class because Python lacks forward declarations.
    :cvar ~._PRECOMPUTE_CONSTANT_SIGNALS: if true a constant expressions
        made from this type have value precomputed.
    """
    _PRECOMPUTE_CONSTANT_SIGNALS = True

    def __init__(self, const=False):
        self.const = const

    def _from_py(self, v, vld_mask):
        """
        same as from_py just without type checks
        """
        return self.getConstCls()._from_py(self, v, vld_mask)

    def from_py(self, v, vld_mask=None):
        """
        Construct value of this type.
        Delegated on value class for this type
        """
        if isinstance(v, Enum):
            v = v.value
        return self.getConstCls().from_py(self, v, vld_mask=vld_mask)

    def auto_cast_HConst(self, const: "HConst", toType: Self) -> Union["RtlSignal", "HConst"]:
        """
        Cast constant of this type to another compatible type.

        :param const: constant to cast
        :param toType: instance of HdlType to cast into
        """
        if const._dtype == toType:
            return const

        try:
            c = self._auto_cast_HConst_fn
        except AttributeError:
            c = self.get_auto_cast_HConst_fn()
            self._auto_cast_HConst_fn = c

        return c(self, const, toType)

    def auto_cast_RtlSignal(self, sig: "RtlSignal", toType: Self) -> Union["RtlSignal", "HConst"]:
        """
        Cast signal of this type to another compatible type.

        :param sig: signal to cast
        :param toType: instance of HdlType to cast into
        """
        if sig._dtype == toType:
            return sig

        try:
            c = self._auto_cast_RtlSignal_fn
        except AttributeError:
            c = self.get_auto_cast_RtlSignal_fn()
            self._auto_cast_RtlSignal_fn = c

        return c(self, sig, toType)

    def reinterpret_cast_HConst(self, const: "HConst", toType):
        """
        Cast constant of this type to another type of same size.

        :param const: constant to cast
        :param toType: instance of HdlType to cast into
        """
        try:
            return self.auto_cast_HConst(const, toType)
        except TypeConversionErr:
            pass

        try:
            r = self._reinterpret_cast_HConst_fn
        except AttributeError:
            r = self.get_reinterpret_cast_HConst_fn()
            self._reinterpret_cast_HConst_fn = r

        return r(self, const, toType)

    def reinterpret_cast_RtlSignal(self, sig: "RtlSignal", toType):
        """
        Cast value or signal of this type to another type of same size.

        :param sig: signal to cast
        :param toType: instance of HdlType to cast into
        """
        try:
            return self.auto_cast_RtlSignal(sig, toType)
        except TypeConversionErr:
            pass

        try:
            r = self._reinterpret_cast_RtlSignal_fn
        except AttributeError:
            r = self.get_reinterpret_cast_RtlSignal_fn()
            self._reinterpret_cast_RtlSignal_fn = r

        return r(self, sig, toType)

    @internal
    @classmethod
    def get_auto_cast_HConst_fn(cls):
        """
        Get method for converting type
        """
        return default_auto_cast_fn

    @internal
    @classmethod
    def get_auto_cast_RtlSignal_fn(cls):
        """
        Get method for converting type
        """
        return default_auto_cast_fn

    @internal
    @classmethod
    def get_reinterpret_cast_HConst_fn(cls):
        """
        Get method for converting type
        """
        return default_reinterpret_cast_fn

    @internal
    @classmethod
    def get_reinterpret_cast_RtlSignal_fn(cls):
        """
        Get method for converting type
        """
        return default_reinterpret_cast_fn

    @internal
    @classmethod
    def getConstCls(cls) -> Type["HConst"]:
        """
        :attention: Overrode in implementation of concrete HdlType.

        :return: class for value derived from this type
        """
        raise NotImplementedError(cls)

    @internal
    @classmethod
    def getRtlSignalCls(cls) -> Type["RtlSignal"]:
        """
        :attention: Overrode in implementation of concrete HdlType.

        :return: class for value derived from this type
        """
        raise NotImplementedError(cls)

    def _as_hdl(self, to_Hdl: "ToHdlAst", declaration):
        raise MethodNotOverloaded()

    def _as_hdl_requires_def(self, to_Hdl: "ToHdlAst", other_types: list):
        raise MethodNotOverloaded()

    def isScalar(self):
        return True

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
        if name is None:
            name = ""
        return f"<{self.__class__.__name__:s} {name:s}>"


@internal
def default_reinterpret_cast_fn(typeFrom: HdlType, sigOrConst: Union["RtlSignal", "HConst"], toType: HdlType):
    raise TypeConversionErr("reinterpret_cast", typeFrom, "->", toType, "is not implemented")


@internal
def default_auto_cast_fn(typeFrom: HdlType, sigOrConst: Union["RtlSignal", "HConst"], toType: HdlType):
    raise TypeConversionErr("auto_cast", typeFrom, "->", toType, "is not implemented")
