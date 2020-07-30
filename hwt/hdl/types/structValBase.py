from hwt.hdl.value import HValue, areHValues
from hwt.serializer.generic.indent import getIndent
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class StructValBase(HValue):
    """
    Base class for values for structure types.
    Every structure type has it's own value class derived from this.
    """
    __slots__ = []

    def __init__(self, typeObj, val, skipCheck=False):
        """
        :param val: None or dict {field name: field value}
        :param typeObj: instance of String HdlType
        :param skipCheck: flag to skip field name consistency in val
        """
        self._dtype = typeObj
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

            if not isinstance(v, (HValue, RtlSignalBase)):
                v = f.dtype.from_py(v)

            setattr(self, f.name, v)

    def __copy__(self):
        d = {}
        for f in self._dtype.fields:
            if f.name is None:
                continue

            v = getattr(self, f.name)
            if not isinstance(v, RtlSignalBase):
                v = v.__copy__()
            d[f.name] = v

        return self.__class__(self._dtype, d, skipCheck=True)

    @classmethod
    def from_py(cls, typeObj, val, vld_mask=None):
        """
        :param val: None or dict {field name: field value}
        :param typeObj: instance of String HdlType
        :param vld_mask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        if vld_mask == 0:
            val = None
        return cls(typeObj, val)

    def to_py(self):
        if not self._is_full_valid():
            raise ValueError("Value of %r is not fully defined" % self)
        d = {}
        for f in self._dtype.fields:
            if f.name is not None:
                val = getattr(self, f.name).to_py()
                d[f.name] = val
        return d

    def __eq__(self, other):
        if areHValues(self, other):
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
            return super(HValue, self).__eq__(other)

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
