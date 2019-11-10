from hwt.code import Concat
from hwt.hdl.typeShortcuts import vec
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import default_reinterpret_cast_fn, HdlType
from hwt.hdl.value import Value
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.doc_markers import internal


@internal
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
                part = f.dtype.from_py(part)

        parts.append(part)

    return Concat(*reversed(parts))


@internal
def hstruct_reinterpret(self, sigOrVal, toType: HdlType):
    if isinstance(toType, Bits):
        return hstruct_reinterpret_to_bits(self, sigOrVal, toType)
    else:
        return default_reinterpret_cast_fn(self, sigOrVal, toType)
