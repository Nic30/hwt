from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.types.structValBase import StructValBase
from hwt.serializer.serializerClases.indent import getIndent


class HStructField(object):
    def __init__(self, typ, name, info=None):
        assert isinstance(name, str) or name is None, name
        assert isinstance(typ, HdlType), typ
        self.name = name
        self.dtype = typ
        self.info = info

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.dtype == other.dtype and
            self.info == other.info
            )

    def __hash__(self):
        return hash((self.dtype, self.name))


class HStruct(HdlType):
    """
    hld structure type

    :ivar fields: tuple of HStructField instances in this struct
    :ivar name: name of this HStruct type
    :ivar isFixedSize: flag which tells if size of this HStruct can resolved or not,
        f.e. field with type of HStream can cause isFixedSize to become False
    :ivar valueCls: Class of value for this type as usual in HdlType implementations
    """
    def __init__(self, *template, name=None):
        """
        :param template: list of tuples (type, name) or HStructField objects
            name can be None it means that there is space in structure
        :param name: optional name used for debugging purposes
        """
        self.fields = []
        self.name = name
        fieldNames = []
        self.isFixedSize = True

        for f in template:
            try:
                field = HStructField(*f)
            except TypeError:
                field = f
            if not isinstance(field, HStructField):
                raise TypeError("Template for struct field %s is not in valid format" % repr(f))

            self.fields.append(field)
            if field.name is not None:
                fieldNames.append(field.name)

            t = field.dtype
            if self.isFixedSize:
                if (isinstance(t, HStruct) and not t.isFixedSize)\
                              or not hasattr(t, "bit_length"):
                    self.isFixedSize = False

        self.fields = tuple(self.fields)
        if self.isFixedSize:
            self.__bit_length_val = self.__bit_length()

        protectedNames = set(["clone", "staticEval", "fromPy", "_dtype"])
        usedNames = set(fieldNames)
        assert not protectedNames.intersection(usedNames), protectedNames.intersection(usedNames)

        class StructVal(StructValBase):
            __slots__ = fieldNames

        self.valueCls = StructVal

    def bit_length(self):
        if self.isFixedSize:
            return self.__bit_length_val
        else:
            raise TypeError("Can not request bit_lenght on size which has not fixed size")

    def __bit_length(self):
        return sum(map(lambda f: f.dtype.bit_length(), self.fields))

    def getValueCls(self):
        return self.valueCls

    def sizeof(self):
        """
        get size of struct in bytes
        """
        s = self.bit_length()

        if s % 8 == 0:
            return s // 8
        else:
            return s // 8 + 1

    def __eq__(self, other):
        return (
            type(self) is type(other) and 
            self.bit_length() == other.bit_length() and
            self.fields == other.fields)

    def __hash__(self):
        return hash((self.name, self.fields))

    def __add__(self, other):
        """
        override of addition, merge struct into one
        """
        assert isinstance(other, HStruct)
        return HStruct(*self.fields, *other.fields)

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not none is used as a additional information about where
            on which address this type is stored (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and Array)
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
                addrTag = " // start:0x%x(bit) 0x%x(byte)" % (withAddr, withAddr // 8)
            else:
                addrTag = ""

            if f.name is None:
                buff.append("%s//%r empty space%s" % (childIndent, f.dtype, addrTag))
            else:
                buff.append("%s %s%s" % (f.dtype.__repr__(indent=indent + 1,
                                                          withAddr=withAddr,
                                                          expandStructs=expandStructs),
                                         f.name, addrTag))
            if withAddr is not None:
                withAddr += f.dtype.bit_length()

        buff.append("%s}" % (myIndent))
        return "\n".join(buff)
