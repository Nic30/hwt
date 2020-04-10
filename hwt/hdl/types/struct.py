from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.structValBase import StructValBase
from hwt.serializer.generic.indent import getIndent


class HStructFieldMeta():
    """
    Meta for field in struct type

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
    def __init__(self, typ, name, meta=None):
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
        return "<HStructField %r, %s>" % (self.dtype, self.name)


protectedNames = {"clone", "staticEval", "from_py", "_dtype"}


class HStruct(HdlType):
    """
    HDL structure type

    :ivar ~.fields: tuple of HStructField instances in this struct
    :ivar ~.name: name of this HStruct type
    :ivar ~.valueCls: Class of value for this type as usual
        in HdlType implementations
    """
    def __init__(self, *template, name=None, const=False):
        """
        :param template: list of tuples (type, name) or HStructField objects
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
                raise TypeError("Template for struct field %s is"
                                " not in valid format" % repr(f))

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
        assert not protectedNames.intersection(usedNames),\
            protectedNames.intersection(usedNames)

        class StructVal(StructValBase):
            __slots__ = list(usedNames)

        if name is not None:
            StructVal.__name__ = name + "Val"

        self.valueCls = StructVal

    def bit_length(self):
        bl = self.__bit_length_val
        if bl is None:
            raise TypeError("Can not request bit_lenght on type"
                            " which has not fixed size")
        else:
            return self.__bit_length_val

    @internal
    def getValueCls(self):
        return self.valueCls

    @internal
    @classmethod
    def get_reinterpret_cast_fn(cls):
        from hwt.hdl.types.structCast import hstruct_reinterpret
        return hstruct_reinterpret

    @internal
    def __fields__eq__(self, other):
        if len(self.fields) != len(other.fields):
            return False
        for sf, of in zip(self.fields, other.fields):
            if (sf.name != of.name or
                    sf.dtype != of.dtype or
                    sf.meta != of.meta):
                return False
        return True

    def __eq__(self, other):
        if self is other:
            return True
        if (type(self) is type(other)):
            if self.name != other.name or self.const != other.const:
                raise False
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
        header = "%sstruct %s{" % (myIndent, name)

        buff = [header, ]
        for f in self.fields:
            if withAddr is not None:
                addrTag = " // start:0x%x(bit) 0x%x(byte)" % (
                            withAddr, withAddr // 8)
            else:
                addrTag = ""

            if f.name is None:
                buff.append("%s//%r empty space%s" % (
                            childIndent, f.dtype, addrTag))
            else:
                buff.append("%s %s%s" % (
                               f.dtype.__repr__(indent=indent + 1,
                                                withAddr=withAddr,
                                                expandStructs=expandStructs),
                            f.name, addrTag))
            if withAddr is not None:
                withAddr += f.dtype.bit_length()

        buff.append("%s}" % (myIndent))
        return "\n".join(buff)
