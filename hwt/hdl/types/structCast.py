from hwt.code import Concat
from hwt.doc_markers import internal
from hwt.hdl.typeShortcuts import vec
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import default_reinterpret_cast_fn, HdlType
from hwt.hdl.value import HValue
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdl.types.array import HArray
from hwt.hdl.types.struct import HStruct


@internal
def hstruct_reinterpret_to_bits(self, sigOrVal, toType: HdlType):
    assert toType.bit_length() == self.bit_length()
    parts = []
    for f in self.fields:
        if f.name is None:
            width = f.dtype.bit_length()
            part = vec(None, width)
        else:
            part = getattr(sigOrVal, f.name)
            if not isinstance(part, (HValue, RtlSignalBase)):
                part = f.dtype.from_py(part)

        parts.append(part)

    return Concat(*reversed(parts))


@internal
def hstruct_reinterpret_using_bits(self, sigOrVal, toType: HdlType):
    as_bits = sigOrVal._reinterpret_cast(Bits(self.bit_length()))
    return as_bits._reinterpret_cast(toType)


@internal
def hstruct_reinterpret(self, sigOrVal, toType: HdlType):
    if isinstance(toType, Bits):
        return hstruct_reinterpret_to_bits(self, sigOrVal, toType)
    elif isinstance(toType, (HStruct, HArray)):
        return hstruct_reinterpret_using_bits(self, sigOrVal, toType)
    else:
        return default_reinterpret_cast_fn(self, sigOrVal, toType)
