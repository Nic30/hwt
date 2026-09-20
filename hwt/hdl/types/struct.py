from typing import Self, TypeVar, Type, Optional

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.structValBase import HStructConstBase, HStructRtlSignalBase, HStructCompatiblePyValT
from hwt.hwIO import HwIO
from hwt.pyUtils.typingFuture import override
from hwt.serializer.generic.indent import getIndent
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal
from hwt.mainBases import RtlSignalBase


class HStructFieldMeta():
    """
    Metadata for a field in :class:`HStruct` type

    :ivar ~.splitMembers: flag which specifies if structured data type of this field
        should be synchronized as a one interface
        or each of it's members should be synchronized separately
    """

    def __init__(self, splitMembers=False):
        self.splitMembers = splitMembers

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        return self.splitMembers == other.splitMembers

    @internal
    def __hash__(self):
        return hash(self.splitMembers)


class HStructField(object):
    """
    Object holding info about a single member in :class:`HStruct` type
    """

    def __init__(self, typ: HdlType, name: str, meta=None):
        assert isinstance(name, str) or name is None, name
        assert isinstance(typ, HdlType), typ
        self.name = name
        self.dtype = typ
        self.meta = meta

    def __eq__(self, other):
        return self.name == other.name and\
               self.dtype == other.dtype and\
               self.meta == other.meta

    def __hash__(self):
        return hash((self.name, self.dtype, self.meta))

    def __repr__(self):
        name = self.name
        if name is None:
            name = "<padding>"

        return f"<HStrructField {self.dtype}, {name:s}>"


_protectedNames = {
    # RtlSignal props
    "_dtype",
    * dir(RtlSignal),
    # HConst
    * dir(HConst),
    # HwIO props
    "_setAttrListener",
    "_associatedClk",
    "_associatedRst",
    "_parent",
    "_name",
    "_masterDir",
    "_direction",
    "_ctx",
    "_isExtern",
    "_ag",
    "_hdlPort",
    "_hdlNameOverride",
    *dir(HwIO),
    # HwIOSignal props
    # "_sig", "_sigInside", "_isAccessible",
    # *dir(HwIOSignal),
}


class HStruct(HdlType):
    """
    HDL structure type

    :ivar ~.fields: tuple of :class:`~.HStructField` instances in this struct
    :ivar ~.name: name of this HStruct type
    :ivar ~.field_by_name: dictionary which maps the name of the field to :class:`~.HStructField` instance
    :ivar ~._constCls: Class of value for this type as usual
        in HdlType implementations
    
    .. code-block::python
        # type definition
        t = HStruct(
            (BIT, "a"), # lower address/sooner in stream
            (BIT, "b"),
        )
        # constant instantiation 
        v = t.from_py({"a": 1, "b":0})
    
    :attention: v._reinterpet_cast(HBits(2)) packs the first member ("a") to a bit 0 (first member at the lowest address as in C)
        Note that this is exactly opposite as in SystemVerilog struct packed {bit a; bit b;}
        where bit "b" would be bit 0    
    
    :ivar _HStructConstBase: base class for HStructConst to allow for instance method re-definion
        for constants of child types
    :ivar _HStructRtlSignalBase: base class for HStructRtlSignal to allow for instance method re-definion
        for constants of child types
        
    .. code-block::python
        # example of use of _HStructConstBase/_HStructRtlSignalBase
        t = HStruct(
            (BIT, "a"),
            (BIT, "b"),
        )
        class MyHStructConstBase(HStructConstBase)
            def any(self):
                return self.a | self.b
        t._HStructConstBase = MyHStructConstBase

        v = t.from_py({"a": 1, "b":0})
        t.any()
    
    """
    _HStructConstBase = HStructConstBase
    _HStructRtlSignalBase = HStructRtlSignalBase

    def __init__(self, *template, name=None, const=False):
        """
        :param template: list of tuples (type, name) or :class:`~.HStructField` objects
            name can be None (= padding)
        :param name: optional name used for debugging purposes
        """
        super(HStruct, self).__init__(const=const)

        fields = []
        field_by_name = {}
        self.name = name
        bit_length = 0
        for f in template:
            try:
                field = HStructField(*f)
            except TypeError:
                field = f
            if not isinstance(field, HStructField):
                raise TypeError(f"Template for struct field ", f, " is"
                                " not in valid format")

            fields.append(field)
            if field.name is not None:
                assert field.name not in field_by_name, field.name
                field_by_name[field.name] = field

            t = field.dtype
            if bit_length is not None:
                try:
                    _bit_length = t.bit_length()
                    bit_length += _bit_length
                except TypeError:
                    bit_length = None

        self.fields = tuple(fields)
        self.field_by_name = field_by_name
        self.__hash = hash((self.name, self.const, self.fields))
        self.__bit_length_val = bit_length

        usedNames = set(field_by_name.keys())
        assert not _protectedNames.intersection(usedNames), \
            _protectedNames.intersection(usedNames)

        class HStructConst(self._HStructConstBase):
            __slots__ = list(usedNames)

        class HStructRtlSignal(self._HStructRtlSignalBase):
            __slots__ = list(usedNames)

        if name is not None:
            HStructConst.__name__ = name + "Const"
            HStructRtlSignal.__name__ = name + "RtlSignal"

        self._constCls = HStructConst
        self._rtlSignalCls = HStructRtlSignal

    def bit_length(self) -> int:
        bl = self.__bit_length_val
        if bl is None:
            raise TypeError("Can not request bit_lenght on type"
                            " which has not fixed size")
        else:
            return self.__bit_length_val

    @internal
    @override
    def getConstCls(self):
        return self._constCls

    @internal
    @override
    def getRtlSignalCls(self):
        """
        :attention: RtlSignal of this class is actually never instantiated and :class:`HwIOStruct` is used instead.
            However the methods of RtlSignal class are called from HwIOStruct.
            This is to have RtlSignal with single HDL id only and to keep RTL level data structures as simple as possible. 
        """
        return self._rtlSignalCls

    @internal
    @classmethod
    def get_reinterpret_cast_HConst_fn(cls):
        from hwt.hdl.types.structCast import hstruct_reinterpret
        return hstruct_reinterpret

    @internal
    @classmethod
    def get_reinterpret_cast_RtlSignal_fn(cls):
        from hwt.hdl.types.structCast import hstruct_reinterpret
        return hstruct_reinterpret

    @internal
    def __fields__eq__(self, other: Self) -> bool:
        if len(self.fields) != len(other.fields):
            return False
        for sf, of in zip(self.fields, other.fields):
            if (sf.name != of.name or
                    sf.dtype != of.dtype or
                    sf.meta != of.meta):
                return False
        return True

    def __eq__(self, other: HdlType) -> bool:
        if self is other:
            return True
        if (type(self) is type(other)):
            if self.name != other.name or self.const != other.const:
                return False
            try:
                self_l = self.bit_length()
            except TypeError:
                self_l = -1
            try:
                other_l = other.bit_length()
            except TypeError:
                other_l = -1

            return self_l == other_l and self.__fields__eq__(other)
        return False

    @internal
    def __hash__(self):
        return self.__hash

    def __add__(self, other):
        """
        override of addition, merge struct into one
        """
        assert isinstance(other, HStruct)
        return HStruct(*self.fields, *other.fields)
    # [todo] method to translate to python cstruct https://stackoverflow.com/a/71118250
    
    @override
    def isScalar(self):
        return False

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and HArray)
        """
        if self.name:
            name = self.name + " "
        else:
            name = ""

        myIndent = getIndent(indent)
        childIndent = getIndent(indent + 1)
        header = f"{myIndent:s}struct {name:s}{{"

        buff = [header, ]
        for f in self.fields:
            if withAddr is not None:
                withAddr_B = withAddr // 8
                addrTag = f" // start:0x{withAddr:x}(bit) 0x{withAddr_B:x}(byte)"
            else:
                addrTag = ""

            if f.name is None:
                buff.append(f"{childIndent:s}//{f.dtype} empty space{addrTag:s}")
            else:
                buff.append("%s %s%s" % (
                               f.dtype.__repr__(indent=indent + 1,
                                                withAddr=withAddr,
                                                expandStructs=expandStructs),
                            f.name, addrTag))
            if withAddr is not None:
                withAddr += f.dtype.bit_length()

        buff.append(f"{myIndent:s}}}")
        return "\n".join(buff)


T = TypeVar("T", bound="HStructFromClass")


class HStructFromClass:
    """
    Base class for struct definitions via class annotations.

    Usage:
    .. code-block::
        class Struct0(HStructFromClass):
            f0: HBits(8)
            f1: HBits(16)

        class Struct1(Struct0):
            __: HBits(8) # nameless padding
            f2: HBits(32)
        
        Struct1.asHdlType() == HStruct(
            (HBits(8), "f0"),
            (HBits(16), "f1"),
            (HBits(8), None),
            (HBits(32), "f2"),
        )
        
        class Struct2(HStructFromClass):
            f0: HBits(8) = 0 # default values are supported
        
        print(Struct2.from_py(None))
        {
           f0: <HBitsConst b8 0>
        }
        # default values can be discarded using vld_mask=0 
        # the values in constructor works as a dict update
        # specifies values override the defaults 
        print(Struct2.from_py(None, vld_mask=0))
        {
           f0: <HBitsConst b8 0, mask 0>
        }
    :attention: all property names has to be unique, and it is not checked
    """

    IGNORED_PADDING_NAME = "__"
    __hStructObj = None
    __hStructObjOrig_from_py = None
    
    @classmethod
    def from_py(cls, val: HStructCompatiblePyValT, vld_mask:Optional[int]=None):
        return cls.asHdlType().from_py(val, vld_mask=vld_mask)
    
    @classmethod
    def _from_py_withInitFromClsDefValues(cls, val: HStructCompatiblePyValT, vld_mask:Optional[int]=None):
        if vld_mask == 0:
            val = None
        else:
            valUpdated = []
            # apply defeault values
            t = cls.__hStructObj
            if isinstance(val, dict):
                for f in t.fields:
                    if f.name is None:
                        continue
                    
                    if val is None:
                        v = None
                    else:
                        v = val.get(f.name, None)
                    
                    if v is None:
                        v = getattr(cls, f.name, None)
        
                    if not isinstance(v, (HConst, HwIO, RtlSignalBase)):
                        v = f.dtype.from_py(v)
                    valUpdated.append(v)
            else:
                if val is None:
                    val = (None for _ in range(len(t.fields)))

                valIt = iter(val)
                for f in t.fields:
                    if f.name is None:
                        continue
                    if val is None:
                        v = None
                    else:
                        v = next(valIt)
        
                    if v is None:
                        v = getattr(cls, f.name, None)
                        
                    if not isinstance(v, (HConst, RtlSignalBase)):
                        v = f.dtype.from_py(v)
                    valUpdated.append(v)
        return cls.__hStructObjOrig_from_py(valUpdated, vld_mask=vld_mask)

    @classmethod
    def asHdlType(cls: type[T]) -> "HStruct":
        hStruct = cls.__dict__.get("_HStructFromClass__hStructObj")  # check that the definition is exactly on this class
        if hStruct is not None:
            return hStruct

        fields = []
        cls._collectHStructFields(fields, {})
        hStruct = HStruct(*fields, name=cls.__name__)
        cls.__hStructObjOrig_from_py = hStruct.from_py
        hStruct.from_py = cls._from_py_withInitFromClsDefValues
        cls.__hStructObj = hStruct
        hStruct.__pyCls__ = cls
        return hStruct

    @classmethod
    def _collectHStructFields(cls, fields: list[tuple[HdlType, str | None]], seenNames: dict[str, Type[Self]]):
        # :note: __mro__ example for Struct0: (Struct0, HStructFromClass, object)
        for base in reversed(cls.__mro__):
            if base is cls or base is object or base is HStructFromClass:
                # skip root pure pyhonic base classes 
                continue

            if not issubclass(base, HStructFromClass):
                continue

            t = base.asHdlType()
            fields.extend(t.fields)
            for f in t.fields:
                if f.name is None:
                    continue
                seenOn = seenNames.get(f.name, None)
                if seenOn is not None:
                    raise AssertionError("The field name is ambiguous", f.name, seenOn, base)
                seenNames[f.name] = base

        annotations = getattr(cls, "__annotations__", None)
        for field_name, typ in annotations.items():
            if isinstance(typ, type) and issubclass(typ, HStructFromClass):
                typ = typ.asHdlType()

            assert isinstance(typ, HdlType), typ

            h_name = None if field_name == cls.IGNORED_PADDING_NAME else field_name
            fields.append((typ, h_name))
            if h_name is not None:
                seenOn = seenNames.get(h_name, None)
                if seenOn is not None:
                    raise AssertionError("The field name is ambiguous", h_name, seenOn, cls)
                seenNames[h_name] = cls

        return fields


def offsetof(structTy: HStruct, field: HStructField):
    """
    Get bit offset field in HStruct
    """
    off = 0
    for f in structTy.fields:
        f: HStructField
        if f is field:
            return off
        else:
            off += f.dtype.bit_length()

    raise AssertionError("field was not found in struct type fields", structTy, field)

