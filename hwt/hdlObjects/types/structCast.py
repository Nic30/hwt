from hwt.code import Concat
from hwt.hdlObjects.typeShortcuts import vec
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.hdlType import default_reinterpret_cast_fn, HdlType
from hwt.hdlObjects.value import Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


def hstruct_reinterpret_to_bits(self, sigOrVal, toType: HdlType):
    assert toType.bit_length() == self.bit_length()
    parts = []
    for f in self.fields:
        if f.name is None:
            width = f.bit_length()
            part = vec(None, width)
        else:
            part = getattr(sigOrVal, f.name)
            if not isinstance(part, (Value, RtlSignalBase)):
                part = f.dtype.fromPy(part)

        parts.append(part)

    return Concat(*reversed(parts))


def hstruct_reinterpret(self, sigOrVal, toType: HdlType):
    if isinstance(toType, Bits):
        return hstruct_reinterpret_to_bits(self, sigOrVal, toType)
    else:
        return default_reinterpret_cast_fn(self, sigOrVal, toType)
