from collections import OrderedDict

from hwt.doc_markers import internal
from hwt.hdl.types.hdlType import HdlType
from hwt.hdl.types.struct import HStructField
from hwt.hdl.value import HValue
from hwt.serializer.generic.indent import getIndent


protectedNames = {"clone", "staticEval",
                  "from_py", "_dtype", "_usedField", "_val"}


class UnionValBase(HValue):
    """
    Base class for values for union types.
    Every union type has it's own value class derived from this.

    :ivar ~._dtype: union type of this value
    :ivar ~.__usedField: member which is actually used to represent value
    :ivar ~.__val: value for __usedField
    """
    __slots__ = ["_dtype", "_val", "_usedField"]

    def __init__(self, typeObj, val):
        """
        :param val: None or tuple (member name, member value)
        :param typeObj: instance of HUnion HdlType for this value
        """
        self._dtype = typeObj
        if val is not None:
            memberName, v = val
        else:
            memberName = next(iter((typeObj.fields.keys())))
            v = None

        f = self._dtype.fields[memberName]
        if not isinstance(v, HValue):
            v = f.dtype.from_py(v)
        else:
            v._auto_cast(f.dtype)
        self._val = v
        self._usedField = f

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        """
        :param val: None or tuple (member name, member value)
        :param typeObj: instance of HUnion HdlType for this value
        :param vld_mask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        if vld_mask == 0:
            val = None
        return cls(typeObj, val)

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


@internal
class HUnionMemberHandler(object):
    """
    Object which manages the acces to HUnion field
    """

    def __init__(self, field):
        self.field = field

    def set(self, parent, v):
        f = parent._dtype.fields[self.field.name]
        if not isinstance(v, HValue):
            v = f.dtype.from_py(v)
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

    :ivar ~.fields: read only OrderedDict {key:StructField} for each
        member in this union
    :ivar ~.name: name of this type
    :ivar ~.__bit_length_val: precalculated bit_length of this type
    """

    def __init__(self, *template, name=None, const=False):
        """
        :param template: list of tuples (type, name) or HStructField objects
            name can be None (= padding)
        :param name: optional name used for debugging purposes
        """
        super(HUnion, self).__init__(const=const)
        self.fields = OrderedDict()
        self.field_by_name = self.fields
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
                raise TypeError(
                    "Template for struct field %s is not"
                    " in valid format" % repr(f))

            assert field.name is not None
            self.fields[field.name] = field

            t = field.dtype
            if bit_length is None:
                bit_length = t.bit_length()
            else:
                _bit_length = t.bit_length()
                if _bit_length != bit_length:
                    raise TypeError(
                        field.name, " has different size than others")

            memberHandler = HUnionMemberHandler(field)
            p = property(fget=memberHandler.get, fset=memberHandler.set)
            setattr(UnionVal, field.name, p)

        self.__bit_length_val = bit_length
        self.__hash = hash((self.name, tuple(self.fields.items())))

        usedNames = set(self.fields.keys())
        assert not protectedNames.intersection(
            usedNames), protectedNames.intersection(usedNames)

        if name is not None:
            UnionVal.__name__ = name + "Val"

        self.valueCls = UnionVal

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
        return self is other or (
            type(self) is type(other) and
            self.bit_length() == other.bit_length() and
            self.__fields__eq__(other))

    @internal
    def __hash__(self):
        return self.__hash

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
                buff.append("%s %s" % (
                                f.dtype.__repr__(indent=indent + 1,
                                                 withAddr=withAddr,
                                                 expandStructs=expandStructs),
                            f.name))

        buff.append("%s}" % (myIndent))
        return "\n".join(buff)
