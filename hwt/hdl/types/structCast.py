from hwt.code import Concat
from hwt.doc_markers import internal
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.hdlType import default_reinterpret_cast_fn, HdlType
from hwt.hdl.types.struct import HStruct
from hwt.hdl.value import HValue
from hwt.interfaces.std import Signal
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


@internal
def hstruct_reinterpret_to_bits(self, sigOrVal, toType: HdlType):
    assert toType.bit_length() == self.bit_length()
    parts = []
    for f in self.fields:
        if f.name is None:
            width = f.dtype.bit_length()
            part = Bits(width).from_py(None)
        else:
            part = getattr(sigOrVal, f.name)
            if isinstance(part, Signal):
                part = part._sig
            if not isinstance(part, (HValue, RtlSignalBase, InterfaceBase)):
                part = f.dtype.from_py(part)
            elif not isinstance(part._dtype, toType.__class__):
                part = part._reinterpret_cast(toType.__class__(part._dtype.bit_length()))

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
