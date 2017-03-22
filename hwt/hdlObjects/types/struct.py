from hwt.hdlObjects.types.hdlType import HdlType


class HStructField(object):
    def __init__(self, name, typ):
        assert isinstance(name, str) or name is None
        self.name = name
        assert isinstance(typ, HdlType)
        self.type = typ


class HStruct(HdlType):
    def __init__(self, *template, name=None):
        """
        @param template: list of tuples (type, name) or HStructField objects
                        name can be None it means that there is space in structure
        @param name: optional name used for debugging purposes
        """
        self.fields = []
        fieldNames = []
        for f in template:
            try:
                typ, name = f
                field = HStructField(name, typ)
            except IndexError:
                if not isinstance(field, HStructField):
                    raise AssertionError("Template for struct field %r is not in valid format" % f)
                field = f
            self.fields.append(field)
            if field.name is not None:
                fieldNames.append(field.name)

        class StructVal(object):
            __structType = self
            __slots__ = fieldNames

            def __init__(self):
                for f in self.__structType.fields:
                    if f.name is not None:
                        setattr(self, f.name, None)

            def __str__(self):
                buff = ["{"]
                for f in self.__structType.fields:
                    if f.name is not None:
                        val = getattr(self, f.name)
                        buff.append("    %s %r" % (f.name, val))
                buff.append("}")
                return "\n".join(buff)

        self.valueCls = StructVal
    
    def bit_length(self):
        return sum(map(lambda f: f.type.bit_length(), self.fields), start=0)
    
    def getValueCls(self):
        return self.valueCls

    def sizeof(self):
        """
        get size of struct in bytes
        """
        s = 0
        for f in self.template:
            s += f.type.bit_length()

        if s % 8 == 0:
            return s // 8
        else:
            return s // 8 + 1
    
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
                buff.append("    //%r empty space" % (f.type))
            else:
                buff.append("    %r %s" % (f.type, f.name))

        buff.append("}")
        return "\n".join(buff)
