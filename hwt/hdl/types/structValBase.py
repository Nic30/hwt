from hwt.hdl.value import Value, areValues
from hwt.serializer.serializerClases.indent import getIndent


class StructValBase(Value):
    """
    Base class for values for structure types.
    Every structure type has it's own value class derived from this.
    """
    __slots__ = []

    def __init__(self, val, typeObj, skipCheck=False):
        self._dtype = typeObj
        self.updateTime = -1
        if not skipCheck and val is not None:
            assert set(self.__slots__).issuperset(set(val.keys())), \
                set(val.keys()).difference(set(self.__slots__))

        for f in self._dtype.fields:
            if f.name is None:
                continue
            if val is None:
                v = None
            else:
                v = val.get(f.name, None)

            if not isinstance(v, Value):
                v = f.dtype.fromPy(v)

            setattr(self, f.name, v)

    def clone(self):
        d = {}
        for f in self._dtype.fields:
            if f.name is None:
                continue

            v = getattr(self, f.name).clone()
            d[f.name] = v

        return self.__class__(d, self._dtype, skipCheck=True)

    @classmethod
    def fromPy(cls, val, typeObj):
        return cls(val, typeObj)

    def __eq__(self, other):
        if areValues(self, other):
            if self._dtype == other._dtype:
                for f in self._dtype.fields:
                    isPadding = f.name is None
                    if not isPadding:
                        sf = getattr(self, f.name)
                        of = getattr(other, f.name)
                        if not (sf == of):
                            return False
                return True
            else:
                return False
        else:
            return super(Value, self).__eq__(other)

    def __repr__(self, indent=0):
        buff = ["{"]
        indentOfFields = getIndent(indent + 1)

        for f in self._dtype.fields:
            if f.name is not None:
                val = getattr(self, f.name)
                try:
                    v = val.__repr__(indent=indent + 1)
                except TypeError:
                    v = repr(val)

                buff.append("%s%s: %s" % (indentOfFields, f.name, v))
        buff.append(getIndent(indent) + "}")
        return ("\n").join(buff)
