from collections import OrderedDict

from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.types.struct import HStructField
from hwt.hdlObjects.value import Value, areValues
from hwt.serializer.serializerClases.indent import getIndent


protectedNames = {"clone", "staticEval", "fromPy", "_dtype", "_usedField", "_val"}


class UnionValBase(Value):
    """
    Base class for values for union types.
    Every union type has it's own value class derived from this.

    :ivar _dtype: union type of this value
    :ivar __usedField: member which is actually used to represent value
    :ivar __val: value for __usedField
    """
    __slots__ = ["_dtype", "_val", "_usedField"]

    def __init__(self, val, typeObj):
        self._dtype = typeObj
        if val is not None:
            memberName, v = val
        else:
            memberName = next(iter((typeObj.fields.keys())))
            v = None

        f = self._dtype.fields[memberName]
        if not isinstance(v, Value):
            v = f.dtype.fromPy(v)
        else:
            v._auto_cast(f.dtype)
        self._val = v
        self._usedField = f

    @classmethod
    def fromPy(cls, val, typeObj):
        return cls(val, typeObj)

    def __eq__(self, other):
        if areValues(self, other):
            if self._dtype == other._dtype:
                otherVal = getattr(other, self.__usedField.name)
                return self.__val == otherVal
            else:
                return False
        else:
            return super(Value, self).__eq__(other)

    def __repr__(self, indent=0):
        buff = ["{"]
        indentOfFields = getIndent(indent + 1)

        for f in self._dtype.fields.values():
            if f.name is not None:
                val = getattr(self, f.name)
                try:
                    v = val.__repr__(indent=indent + 1)
                except TypeError:
                    v = repr(val)

                buff.append("%s%s: %s" % (indentOfFields, f.name, v))
        buff.append(getIndent(indent) + "}")
        return ("\n").join(buff)


class HUnionMemberHandler(object):

    def __init__(self, field):
        self.field = field

    def set(self, parent, v):
        f = parent._dtype.fields[self.field.name]
        if not isinstance(v, Value):
            v = f.dtype.fromPy(v)
        else:
            v._auto_cast(f.dtype)

        parent._val = v
        parent._usedField = f

    def get(self, parent):
        name = self.field.name
        v = parent._val
        if parent._usedField.name == name:
            return v
        else:
            f = parent._dtype.fields[name]
            v = v._reinterpret_cast(f.dtype)
            parent._val = v
            parent._usedField = f
            return v


class HUnion(HdlType):
    """
    HDL union type (same data multiple representations)

    :ivar fields: read only OrderedDict {key:StructField} for each
        member in this union
    :ivar name: name of this type
    :ivar __bit_length_val: precalculated bit_length of this type
    """
    def __init__(self, *template, name=None):
        """
        :param template: list of tuples (type, name) or HStructField objects
            name can be None (= padding)
        :param name: optional name used for debugging purposes
        """
        self.fields = OrderedDict()
        self.name = name
        bit_length = None

        class UnionVal(UnionValBase):
            pass

        for f in template:
            try:
                field = HStructField(*f)
            except TypeError:
                field = f
            if not isinstance(field, HStructField):
                raise TypeError("Template for struct field %s is not in valid format" % repr(f))

            assert field.name is not None
            self.fields[field.name] = field

            t = field.dtype
            if bit_length is None:
                bit_length = t.bit_length()
            else:
                _bit_length = t.bit_length()
                if _bit_length != bit_length:
                    raise TypeError(field.name, " has different size than others")

            memberHandler = HUnionMemberHandler(field)
            p = property(fget=memberHandler.get, fset=memberHandler.set)
            setattr(UnionVal, field.name, p)

        self.fields = self.fields
        self.__bit_length_val = bit_length

        usedNames = set(self.fields.keys())
        assert not protectedNames.intersection(usedNames), protectedNames.intersection(usedNames)

        if name is not None:
            UnionVal.__name__ = name + "Val"

        self.valueCls = UnionVal

    def bit_length(self):
        bl = self.__bit_length_val
        if bl is None:
            raise TypeError("Can not request bit_lenght on size"
                            " which has not fixed size")
        else:
            return self.__bit_length_val

    def getValueCls(self):
        return self.valueCls

    def __fields__eq__(self, other):
        if len(self.fields) != len(other.fields):
            return False

        for k, sf in self.fields.items():
            try:
                of = other.fields[k]
            except KeyError:
                return False

            if (sf.dtype != of.dtype or
                    sf.meta != of.meta):
                return False

        return True

    def __eq__(self, other):
        return (
            type(self) is type(other) and
            self.bit_length() == other.bit_length() and
            self.__fields__eq__(other))

    def __hash__(self):
        return hash(id(self))

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
        header = "%sunion %s{" % (myIndent, name)

        buff = [header, ]
        for f in self.fields.values():
            if f.name is None:
                buff.append("%s//%r empty space" % (childIndent, f.dtype))
            else:
                buff.append("%s %s" % (f.dtype.__repr__(indent=indent + 1,
                                                        withAddr=withAddr,
                                                        expandStructs=expandStructs),
                                       f.name))

        buff.append("%s}" % (myIndent))
        return "\n".join(buff)
