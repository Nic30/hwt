from typing import Optional

from hwt.hdl.const import HConst
from hwt.mainBases import RtlSignalBase
from hwt.serializer.generic.indent import getIndent
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class HStructRtlSignalBase(RtlSignal):
    __slots__ = []

    def __repr__(self, indent=0):
        return HStructConstBase.__repr__(indent=indent)


class HStructConstBase(HConst):
    """
    Base class for values for structure types.
    Every structure type has it's own value class derived from this.
    """
    __slots__ = []

    def __init__(self, typeObj: "HStruct", val: Optional[dict], skipCheck=False):
        """
        :param val: None or dict {field name: field value}
        :param typeObj: instance of HString HdlType
        :param skipCheck: flag to skip field name consistency in val
        """
        self._dtype = typeObj
        if not skipCheck and val is not None:
            assert set(self.__slots__).issuperset(set(val.keys())), \
                ("struct value specifies undefined members",
                 set(val.keys()).difference(set(self.__slots__)))

        for f in self._dtype.fields:
            if f.name is None:
                continue
            if val is None:
                v = None
            else:
                v = val.get(f.name, None)

            if not isinstance(v, (HConst, RtlSignalBase)):
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
        :param typeObj: instance of HString HdlType
        :param vld_mask: if is None validity is resolved from val
            if is 0 value is invalidated
            if is 1 value has to be valid
        """
        if vld_mask == 0:
            val = None
        return cls(typeObj, val)

    def _is_full_valid(self):
        for f in self._dtype.fields:
            if f.name is not None:
                val = getattr(self, f.name, None)
                if val is None or not val._is_full_valid():
                    return False
        return True

    def _is_partially_valid(self) -> bool:
        for f in self._dtype.fields:
            if f.name is not None:
                val = getattr(self, f.name, None)
                if val is None and val._is_partially_valid():
                    return True
        return False

    def to_py(self):
        if not self._is_full_valid():
            raise ValueError(f"Value of {self} is not fully defined")
        d = {}
        for f in self._dtype.fields:
            if f.name is not None:
                val = getattr(self, f.name).to_py()
                d[f.name] = val
        return d

    def __ne__(self, other):
        if isinstance(other, HConst):
            if self._dtype == other._dtype:
                for f in self._dtype.fields:
                    isPadding = f.name is None
                    if not isPadding:
                        sf = getattr(self, f.name)
                        of = getattr(other, f.name)
                        if (sf != of):
                            return True
                return False
            else:
                return True
        else:
            return super(HConst, self).__ne__(other)

    def _eq(self, other):
        return self.__eq__(other)

    def __eq__(self, other):
        if isinstance(other, HConst):
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
            return super(HConst, self).__eq__(other)

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

                buff.append(f"{indentOfFields:s}{f.name:s}: {v:s}")

        buff.append(getIndent(indent) + "}")
        return ("\n").join(buff)

