from typing import Union

from hwt.code import Concat
from hwt.doc_markers import internal
from hwt.hObjList import HObjList
from hwt.hdl.const import HConst
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.hdlType import HdlType, default_reinterpret_cast_fn
from hwt.hdl.types.struct import HStruct
from hwt.hwIOs.std import HwIOSignal
from hwt.mainBases import HwIOBase
from hwt.mainBases import RtlSignalBase


@internal
def hstruct_reinterpret_to_bits(self: HStruct, sigOrConst: Union[RtlSignalBase, HConst], toType: HdlType):
    assert toType.bit_length() == self.bit_length()
    parts = []
    for f in self.fields:
        if f.name is None:
            width = f.dtype.bit_length()
            part = HBits(width).from_py(None)
        else:
            part = getattr(sigOrConst, f.name)
            if isinstance(part, HwIOSignal):
                part = part._sig

            if isinstance(part, HObjList):
                elmTyFlat = HBits(f.dtype.element_t.bit_length())
                for partPart in part:
                    pp = partPart._reinterpret_cast(elmTyFlat)
                    parts.append(pp)
                continue
            elif not isinstance(part, (HConst, RtlSignalBase, HwIOBase)):
                part = f.dtype.from_py(part)
            elif not isinstance(part._dtype, toType.__class__):
                part = part._reinterpret_cast(toType.__class__(part._dtype.bit_length()))
            # else add part as is
            assert isinstance(part._dtype, HBits), part

        parts.append(part)

    return Concat(*reversed(parts))


@internal
def hstruct_reinterpret_using_bits(self: HStruct, sigOrConst: Union[RtlSignalBase, HConst], toType: HdlType):
    as_bits = sigOrConst._reinterpret_cast(HBits(self.bit_length()))
    return as_bits._reinterpret_cast(toType)


@internal
def hstruct_reinterpret(self: HStruct, sigOrConst: Union[RtlSignalBase, HConst], toType: HdlType):
    if isinstance(toType, HBits):
        return hstruct_reinterpret_to_bits(self, sigOrConst, toType)
    elif isinstance(toType, (HStruct, HArray)):
        return hstruct_reinterpret_using_bits(self, sigOrConst, toType)
    else:
        return default_reinterpret_cast_fn(self, sigOrConst, toType)
