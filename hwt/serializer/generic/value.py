from copy import copy
from typing import Union

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlValueInt, HdlDirection
from hwt.hdl.types.array import HArray
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import INT, BOOL
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.slice import Slice
from hwt.hdl.types.string import String
from hwt.hdl.value import HValue
from hwt.hdl.variables import SignalItem
from hwt.serializer.exceptions import SerializerException
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase


class ToHdlAst_Value():

    def is_suitable_for_const_extract(self, val: HValue):
        """
        :return: True if an value should be extracted as a constant if possible
        """
        return False

    def as_hdl_Value(self, val):
        """
        :param dst: is signal connected with value
        :param val: value object, can be instance of Signal or HValue
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

        if isinstance(t, Slice):
            return self.as_hdl_SliceVal(val)
        elif isinstance(t, HArray):
            return self.as_hdl_HArrayVal(val)
        elif isinstance(t, Bits):
            return self.as_hdl_BitsVal(val)
        elif isinstance(t, HEnum):
            return self.as_hdl_HEnumVal(val)
        elif isinstance(t, String):
            return self.as_hdl_StringVal(val)
        else:
            raise SerializerException(
                "can not resolve value serialization for %r"
                % (val))

    def as_hdl_int(self, val: int):
        assert isinstance(val, int), val
        return HdlValueInt(val, None, None)

    def Value_try_extract_as_const(self, val):
        return None

    def as_hdl_IntegerVal(self, val):
        return self.as_hdl_int(int(val.val))

    def as_hdl_BitsVal(self, val):
        t = val._dtype
        if t == INT:
            return self.as_hdl_IntegerVal(val)
        elif t == BOOL:
            return self.as_hdl_BoolVal(val)
        w = t.bit_length()
        return self.as_hdl_BitString(val.val, w, t.force_vector,
                                     val.vld_mask, t.signed)

    def as_hdl_StringVal(self, val):
        return val.val

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
                            "Signal %s is constant and has undefined value"
                            % si.name)
                    var.is_const = True
                else:
                    raise SerializerException(
                        "Signal %s should be declared but it is not used"
                        % si.name)

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
            elif isinstance(v, HValue):
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
            if si.hidden and hasattr(si, "origin"):
                # hidden signal, render it's driver instead
                return self.as_hdl(si.origin)
            return HdlValueId(si.name, obj=si)
