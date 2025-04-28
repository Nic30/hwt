from enum import Enum
from typing import Union, Type, Self, Optional

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

    :ivar const: if True the type has const specifier which means that the value
        should not be modified after initialization and is read only
    :note: Cast functions are linked trough HldType class because Python lacks forward declarations.
    :cvar ~._PRECOMPUTE_CONSTANT_SIGNALS: if true a constant expressions
        made from this type have value pre-computed.
    
    :note: Each implementation of HdlType also defines is HConst and RtlSignal class.
        These classes then implement operators and methods for constants/expressions.
    """
    _PRECOMPUTE_CONSTANT_SIGNALS = True

    def __init__(self, const=False):
        self.const = const

    def _from_py(self, v, vld_mask) -> "HConst":
        """
        same as from_py just without type checks
        """
        return self.getConstCls()._from_py(self, v, vld_mask)

    def from_py(self, v, vld_mask=None) -> "HConst":
        """
        Construct value of this type.
        Delegated on value class for this type
        """
        if isinstance(v, Enum):
            v = v.value
        return self.getConstCls().from_py(self, v, vld_mask=vld_mask)

    def auto_cast_HConst(self, v: "HConst", toType: Self) -> "HConst":
        """
        Cast constant of this type to another compatible type.
        :note: auto cast may change bitwidth if type
            implements it in auto cast

        :param v: constant to cast
        :param toType: instance of HdlType to cast into
        """
        if v._dtype == toType:
            return v

        try:
            castFn = self._auto_cast_HConst_fn
        except AttributeError:
            castFn = self.get_auto_cast_HConst_fn()
            self._auto_cast_HConst_fn = castFn

        try:
            return castFn(self, v, toType)
        except TypeConversionErr:
            pass
        return toType._reverse_auto_cast_HConst(v, self)

    def auto_cast_RtlSignal(self, v: "RtlSignal", toType: Self) -> "RtlSignal":
        """
        Equivalent of :meth:`~.auto_cast_HConst` for :class:`RtlSignal` instances
        """
        if v._dtype == toType:
            return v

        try:
            castFn = self._auto_cast_RtlSignal_fn
        except AttributeError:
            castFn = self.get_auto_cast_RtlSignal_fn()
            self._auto_cast_RtlSignal_fn = castFn

        try:
            return castFn(self, v, toType)
        except TypeConversionErr:
            pass
        return toType._reverse_auto_cast_RtlSignal(v, self)

    def reinterpret_cast_HConst(self, v: "HConst", toType: Self) -> "HConst":
        """
        Cast constant of this type to another type of same size.

        :param v: constant to cast
        :param toType: instance of HdlType to cast into
        """
        if v._dtype == toType:
            return v

        try:
            castFn = self._reinterpret_cast_HConst_fn
        except AttributeError:
            castFn = self.get_reinterpret_cast_HConst_fn()
            self._reinterpret_cast_HConst_fn = castFn

        try:
            return castFn(self, v, toType)
        except TypeConversionErr:
            pass
        return toType._reverse_reinterpret_cast_HConst(v, self)

    def reinterpret_cast_RtlSignal(self, v: "RtlSignal", toType: Self) -> "RtlSignal":
        """
        Cast value or signal of this type to another type of same size.

        :param v: signal to cast
        :param toType: instance of HdlType to cast into
        """
        if v._dtype == toType:
            return v

        try:
            castFn = self._reinterpret_cast_RtlSignal_fn
        except AttributeError:
            castFn = self.get_reinterpret_cast_RtlSignal_fn()
            self._reinterpret_cast_RtlSignal_fn = castFn

        try:
            # call _reinterpret_cast_RtlSignal_fn to cast this type to toType
            return castFn(self, v, toType)
        except TypeConversionErr:
            pass

        return toType._reverse_reinterpret_cast_RtlSignal(v, self)

    # reverse casts which are doing the same thing but cast methods are implemented on dst type
    # :note: this is there to allow casting old types(self) to a new types(toType)
    #   when old type does not know anything about new type
    def _reverse_auto_cast_HConst(self, v: "HConst", fromType: Self) -> "HConst":
        try:
            castFn = self._reverse_auto_cast_HConst_fn
        except AttributeError:
            castFn = self.get_reverse_auto_cast_HConst_fn()
            self._reverse_auto_cast_HConst_fn = castFn

        return castFn(self, v, fromType)

    def _reverse_auto_cast_RtlSignal(self, v: "RtlSignal", fromType: Self) -> "RtlSignal":
        try:
            castFn = self._reverse_auto_cast_RtlSignal_fn
        except AttributeError:
            castFn = self.get_reverse_auto_cast_RtlSignal_fn()
            self._reverse_auto_cast_RtlSignal_fn = castFn

        return castFn(self, v, fromType)

    def _reverse_reinterpret_cast_HConst(self, v: "HConst", fromType: Self) -> "HConst":
        try:
            castFn = self._reverse_reinterpret_cast_HConst_fn
        except AttributeError:
            castFn = self.get_reverse_reinterpret_cast_HConst_fn()
            self._reverse_reinterpret_cast_HConst_fn = castFn

        return castFn(self, v, fromType)

    def _reverse_reinterpret_cast_RtlSignal(self, v: "RtlSignal", fromType: Self) -> "RtlSignal":
        try:
            castFn = self._reverse_reinterpret_cast_RtlSignal_fn
        except AttributeError:
            castFn = self.get_reverse_reinterpret_cast_RtlSignal_fn()
            self._reverse_reinterpret_cast_RtlSignal_fn = castFn

        return castFn(self, v, fromType)

    # methods for getting cast function which cast value of one type to another
    # for more details :see: methods for casting of this class
    @internal
    @classmethod
    def get_auto_cast_HConst_fn(cls):
        return default_auto_cast_fn

    @internal
    @classmethod
    def get_auto_cast_RtlSignal_fn(cls):
        return default_auto_cast_fn

    @internal
    @classmethod
    def get_reverse_auto_cast_RtlSignal_fn(cls):
        return default_reverse_auto_cast_fn

    @internal
    @classmethod
    def get_reverse_auto_cast_HConst_fn(cls):
        return default_reverse_auto_cast_fn

    @internal
    @classmethod
    def get_reinterpret_cast_HConst_fn(cls):
        return default_reinterpret_cast_fn

    @internal
    @classmethod
    def get_reverse_reinterpret_cast_HConst_fn(cls):
        return default_reverse_reinterpret_cast_fn

    @internal
    @classmethod
    def get_reinterpret_cast_RtlSignal_fn(cls):
        return default_reinterpret_cast_fn

    @internal
    @classmethod
    def get_reverse_reinterpret_cast_RtlSignal_fn(cls):
        return default_reverse_reinterpret_cast_fn

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

    def _as_hdl(self, to_Hdl: "ToHdlAst", declaration:bool):
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

    def __repr__(self, indent:int=0, withAddr:Optional[int]=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None, it is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and Array)
        """
        name = getattr(self, "name", "")
        if name is None:
            name = ""
        return f"<{self.__class__.__name__:s} {name:s}>"


@internal
def default_auto_cast_fn(typeFrom: HdlType, sigOrConst: Union["RtlSignal", "HConst"], toType: HdlType):
    raise TypeConversionErr("auto_cast", typeFrom, "->", toType, "is not implemented")


@internal
def default_reverse_auto_cast_fn(toType: HdlType, sigOrConst: Union["RtlSignal", "HConst"], fromType: HdlType):
    raise TypeConversionErr("auto_cast", fromType, "->", toType, "is not implemented")


@internal
def default_reinterpret_cast_fn(fromType: HdlType, sigOrConst: Union["RtlSignal", "HConst"], toType: HdlType):
    raise TypeConversionErr("reinterpret_cast", fromType, "->", toType, "is not implemented")


@internal
def default_reverse_reinterpret_cast_fn(toType: HdlType, sigOrConst: Union["RtlSignal", "HConst"], fromType: HdlType):
    raise TypeConversionErr("reinterpret_cast", fromType, "->", toType, "is not implemented")
