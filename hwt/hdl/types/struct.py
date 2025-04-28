from typing import Self

from hwt.doc_markers import internal
from hwt.hdl.const import HConst
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.structValBase import HStructConstBase, HStructRtlSignalBase
from hwt.hwIO import HwIO
from hwt.pyUtils.typingFuture import override
from hwt.serializer.generic.indent import getIndent
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class HStructFieldMeta():
    """
    Metadata for a field in :class:`HStruct` type

    :ivar ~.split: flag which specifies if structured data type of this field
        should be synchronized as a one interface
        or each it's part should be synchronized separately
    """

    def __init__(self, split=False):
        self.split = split

    def __eq__(self, other):
        if other is None:
            return False
        return self.split == other.split

    @internal
    def __hash__(self):
        return hash(self.split)


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

        return f"<HStructField {self.dtype}, {name:s}>"


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
            (BIT, "a"),
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
                raise TypeError(f"Template for struct field {f} is"
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

