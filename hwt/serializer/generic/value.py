from copy import copy
from typing import Union

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlValueInt, HdlDirection
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.bitsConst import HBitsConst
from hwt.hdl.types.defs import INT, BOOL, FLOAT64
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.float import HFloat
from hwt.hdl.types.function import HFunction, HFunctionConst
from hwt.hdl.types.slice import HSlice
from hwt.hdl.types.string import HString
from hwt.hdl.types.stringConst import HStringConst
from hwt.hdl.const import HConst
from hwt.hdl.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.mainBases import RtlSignalBase


class ToHdlAst_Value():

    def is_suitable_for_const_extract(self, val: HConst):
        """
        :return: True if an value should be extracted as a constant if possible
        """
        return False

    def as_hdl_Value(self, val):
        """
        :param dst: is signal connected with value
        :param val: value object, can be instance of Signal or HConst
        """
        t = val._dtype
        if isinstance(val, RtlSignalBase):
            return self.as_hdl_SignalItem(val)

        # try to extract value as constant
        cc = self.constCache
        if cc is not None:
            if self.is_suitable_for_const_extract(val):
                c = cc.extract_const_val_as_const_var(val)
                if c is not None:
                    return self.as_hdl(c)

        if isinstance(t, HSlice):
            return self.as_hdl_HSliceConst(val)
        elif isinstance(t, HArray):
            return self.as_hdl_HArrayConst(val)
        elif isinstance(t, HBits):
            return self.as_hdl_HBitsConst(val)
        elif isinstance(t, HEnum):
            return self.as_hdl_HEnumConst(val)
        elif isinstance(t, HString):
            return self.as_hdl_HStringConst(val)
        elif isinstance(t, HFloat):
            return self.as_hdl_HFloatConst(val)
        elif isinstance(t, HFunction):
            return self.as_hdl_HFunctionConst(val)
        else:
            raise SerializerException(
                "can not resolve value serialization for %r"
                % (val))

    def as_hdl_int(self, val: int):
        assert isinstance(val, int), val
        return HdlValueInt(val, None, None)

    def Value_try_extract_as_const(self, val):
        return None

    def as_hdl_IntegerVal(self, val: HBitsConst):
        return self.as_hdl_int(int(val.val))

    def as_hdl_HBitsConst(self, val: HBitsConst):
        t = val._dtype
        if t == INT:
            return self.as_hdl_IntegerVal(val)
        elif t == BOOL:
            return self.as_hdl_HBoolConst(val)
        w = t.bit_length()
        return self.as_hdl_BitString(val.val, w, t.force_vector,
                                     val.vld_mask, t.signed)

    def as_hdl_HStringConst(self, val: HStringConst):
        return val.val

    def as_hdl_HFunctionConst(self, val: HFunctionConst):
        return val.val

    def as_hdl_HFloatConst(self, val):
        if val._dtype != FLOAT64:
            raise NotImplementedError(val._dtype)
        return float(val)

    def as_hdl_SignalItem(self, si: Union[SignalItem, HdlIdDef],
                          declaration=False):
        if declaration:
            if isinstance(si, HdlIdDef):
                var = copy(si)
                si = si.origin
            else:
                var = HdlIdDef()
                var.name = si.name
                var.origin = si
                var.value = si._val
                var.type = si._dtype
                var.is_const = si._const
            v = var.value
            if isinstance(si, RtlSignalBase):
                if si.virtual_only:
                    var.is_latched = True
                elif si.drivers or var.direction != HdlDirection.UNKNOWN:
                    # has drivers or is port/param
                    pass
                elif si.endpoints:
                    if not v.vld_mask:
                        raise SerializerException(
                            f"Signal {si.name:s} is constant and has undefined value")
                    var.is_const = True
                else:
                    raise SerializerException(
                        f"Signal {si.name:s} should be declared but it is not used")

            if v is None:
                pass
            elif isinstance(v, RtlSignalBase):
                if v._const:
                    var.value = self.as_hdl(v)
                else:
                    # default value has to be set by reset,
                    # because it is not resolvable in compile time
                    var.value = None
                    pass
            elif isinstance(v, HConst):
                if v.vld_mask or var.is_const:
                    orig_const_cache = self.constCache
                    try:
                        self.constCache = None
                        var.value = self.as_hdl_Value(v)
                    finally:
                        self.constCache = orig_const_cache
                else:
                    # remove value if it is entirely undefined
                    var.value = None
            else:
                raise NotImplementedError(v)
            var.type = self.as_hdl_HdlType(var.type)
            return var
        else:
            if si.hidden and si.origin is not None:
                # hidden signal, render it's driver instead
                return self.as_hdl(si.origin)
            return HdlValueId(si.name, obj=si)
