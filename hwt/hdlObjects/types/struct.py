from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.value import Value


class HStructField(object):
    def __init__(self, typ, name, info=None):
        assert isinstance(name, str) or name is None, name
        assert isinstance(typ, HdlType), typ
        self.name = name
        self.dtype = typ
        self.info = info

    def __hash__(self):
        return hash((self.dtype, self.name))


class HStruct(HdlType):
    """
    C-like structure type

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

        class StructVal(Value):
            __slots__ = fieldNames

            def __init__(self, val, typeObj):
                self._dtype = typeObj

                for f in self._dtype.fields:
                    if f.name is None:
                        continue
                    v = val.get(f.name, None)
                    if not isinstance(v, Value):
                        v = f.dtype.fromPy(v)
                    setattr(self, f.name, v)

            @classmethod
            def fromPy(cls, val, typeObj):
                self = cls(val, typeObj)
                return self

            def __repr__(self):
                buff = ["{"]
                for f in self._dtype.fields:
                    if f.name is not None:
                        val = getattr(self, f.name)
                        buff.append("    %s %r" % (f.name, val))
                buff.append("}")
                return "\n".join(buff)

        protectedNames = set(["clone", "staticEval", "fromPy", "_dtype"])
        usedNames = set(fieldNames)
        assert not protectedNames.intersection(usedNames), protectedNames.intersection(usedNames)

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
        s = 0
        for f in self.template:
            s += f.dtype.bit_length()

        if s % 8 == 0:
            return s // 8
        else:
            return s // 8 + 1

    def __hash__(self):
        return hash((self.name, self.fields))

    def __add__(self, other):
        """
        override of addition, merge struct into one
        """
        assert isinstance(other, HStruct)
        return HStruct(*self.fields, *other.fields)

    def __str__(self):
        if self.name:
            name = self.name + " "
        else:
            name = ""

        buff = ["struct %s{" % name]
        for f in self.fields:
            if f.name is None:
                buff.append("    //%r empty space" % (f.dtype))
            else:
                buff.append("    %r %s" % (f.dtype, f.name))

        buff.append("}")
        return "\n".join(buff)
