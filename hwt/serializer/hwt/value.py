from typing import Union

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueInt, HdlOp, HdlOpType,\
    HdlValueId
from hdlConvertorAst.translate._verilog_to_basic_hdl_sim_model.utils import hdl_getattr,\
    hdl_call
from hdlConvertorAst.translate.common.name_scope import ObjectForNameNotFound
from hwt.hdl.types.arrayVal import HArrayVal
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.defs import SLICE
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.variables import SignalItem
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.serializer.simModel.value import ToHdlAstSimModel_value
from hwt.hdl.value import HValue
from copy import copy


class ToHdlAstHwt_value(ToHdlAst_Value):
    NONE = HdlValueId("None")
    SLICE = HdlValueId("SLICE", obj=SLICE)

    def is_suitable_for_const_extract(self, val: HValue):
        # full valid values can be represented as int and do not have any
        # constructor overhead, entirely invalid values can be represented by None
        return not val._is_full_valid() and not isinstance(val._dtype, HEnum)

    def as_hdl_BitsVal(self, val: BitsVal):
        isFullVld = val._is_full_valid()
        if not self._valueWidthRequired:
            if isFullVld:
                return HdlValueInt(val.val, None, 16)
            elif val.vld_mask == 0:
                return self.NONE

        t = self.as_hdl_HdlType_bits(val._dtype, declaration=False)
        c = hdl_getattr(t, "from_py")
        args = [HdlValueInt(val.val, None, 16), ]
        if not isFullVld:
            args.append(HdlValueInt(val.vld_mask, None, 16))

        return hdl_call(c, args)

    def as_hdl_SignalItem(self, si: Union[SignalItem, HdlIdDef], declaration=False):
        if declaration:
            if isinstance(si, HdlIdDef):
                new_si = copy(si)
                new_si.type = self.as_hdl_HdlType(si.type)
                if si.value is not None:
                    new_si.value = self.as_hdl_Value(si.value)
                return new_si
            else:
                raise NotImplementedError()
        else:
            # if isinstance(si, SignalItem) and si._const:
            #    # to allow const cache to extract constants
            #    return self.as_hdl_Value(si._val)
            if si.hidden and hasattr(si, "origin"):
                return self.as_hdl(si.origin)
            else:
                return HdlValueId(si.name, obj=si)

    def as_hdl_DictVal(self, val):
        return ToHdlAstSimModel_value.as_hdl_DictVal(self, val)

    def as_hdl_HArrayVal(self, val: HArrayVal):
        if not val.vld_mask:
            return self.NONE
        # else:
        #    if len(val.val) == val._dtype.size:
        #        allValuesSame = True
        #        values = iter(val.val.values())
        #        reference = next(values)
        #         for v in values:
        #             if allValuesSame:
        #                 allValuesSame = isSameHVal(reference, v)
        #             else:
        #                 break
        #        if allValuesSame:
        #            # all values of items in array are same, use generator
        #            # exression
        #            raise NotImplementedError()
        #            return "[%s for _ in range(%d)]" % (self.Value(reference))

        # if value can not be simplified it is required to serialize it item
        # by item
        return self.as_hdl_DictVal(val.val)

    def as_hdl_SliceVal(self, val: SliceVal):
        if val._is_full_valid():
            return HdlOp(
                HdlOpType.DOWNTO, [
                    HdlValueInt(int(val.val.start), None, None),
                    HdlValueInt(int(val.val.stop), None, None)
                ])
        else:
            raise NotImplementedError()
            return "SliceVal(slice(%s, %s, %s), SLICE, %d)" % (
                self.as_hdl_Value(val.val.start),
                self.as_hdl_Value(val.val.stop),
                self.as_hdl_Value(val.val.step),
                val.vld_mask)

    def as_hdl_HEnumVal(self, val: HEnumVal):
        try:
            t_name = self.name_scope.get_object_name(val._dtype)
        except ObjectForNameNotFound:
            if self.debug:
                t_name = val._dtype.name
            else:
                raise

        if val.vld_mask:
            try:
                name = self.name_scope.get_object_name(val)
            except ObjectForNameNotFound:
                if self.debug:
                    name = val.val
                else:
                    raise

            return hdl_getattr(HdlValueId(t_name, obj=val._dtype), name)
        else:
            return hdl_call(hdl_getattr(HdlValueId(t_name, obj=val._dtype), "from_py"),
                            [None, ])
