from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.types.struct import HStructField
from hwt.serializer.serializerClases.indent import getIndent


protectedNames = {"clone", "staticEval", "fromPy", "_dtype"}


class HUnion(HdlType):
    """
    HDL union type (same data multiple representations)
    """
    def __init__(self, *template, name=None):
        """
        :param template: list of tuples (type, name) or HStructField objects
            name can be None (= padding)
        :param name: optional name used for debugging purposes
        """
        self.fields = []
        self.name = name
        fieldNames = []
        bit_length = None
        for f in template:
            try:
                field = HStructField(*f)
            except TypeError:
                field = f
            if not isinstance(field, HStructField):
                raise TypeError("Template for struct field %s is not in valid format" % repr(f))

            self.fields.append(field)
            assert field.name is not None
            fieldNames.append(field.name)

            t = field.dtype
            if bit_length is None:
                bit_length = t.bit_length()
            else:
                _bit_length = t.bit_length()
                if _bit_length != bit_length:
                    raise TypeError(field.name, " has different size than others")

        self.fields = tuple(self.fields)
        self.__bit_length_val = bit_length

        usedNames = set(fieldNames)
        assert not protectedNames.intersection(usedNames), protectedNames.intersection(usedNames)

        class UnionVal():
            __slots__ = fieldNames

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
        for sf, of in zip(self.fields, other.fields):
            if (sf.name != of.name or
                    sf.dtype != of.dtype or
                    sf.meta != of.meta):
                return False
        return True

    def __eq__(self, other):
        return (
            type(self) is type(other) and 
            self.bit_length() == other.bit_length() and
            self.__fields__eq__(other))

    def __hash__(self):
        return hash((self.name, self.fields))

    def __repr__(self, indent=0, withAddr=None, expandStructs=False):
        """
        :param indent: number of indentation
        :param withAddr: if is not None is used as a additional
            information about on which address this type is stored
            (used only by HStruct)
        :param expandStructs: expand HStructTypes (used by HStruct and Array)
        """
        if self.name:
            name = self.name + " "
        else:
            name = ""

        myIndent = getIndent(indent)
        childIndent = getIndent(indent + 1)
        header = "%sunion %s{" % (myIndent, name)

        buff = [header, ]
        for f in self.fields:
            if f.name is None:
                buff.append("%s//%r empty space" % (childIndent, f.dtype))
            else:
                buff.append("%s %s" % (f.dtype.__repr__(indent=indent + 1,
                                                        withAddr=withAddr,
                                                        expandStructs=expandStructs),
                                       f.name))

        buff.append("%s}" % (myIndent))
        return "\n".join(buff)
