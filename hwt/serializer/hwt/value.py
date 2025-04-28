from copy import copy
from typing import Union

from hdlConvertorAst.hdlAst._defs import HdlIdDef
from hdlConvertorAst.hdlAst._expr import HdlValueInt, HdlOp, HdlOpType, \
    HdlValueId
from hdlConvertorAst.translate.common.name_scope import ObjectForNameNotFound
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_getattr, \
    hdl_call
from hwt.hdl.const import HConst
from hwt.hdl.types.arrayConst import HArrayConst
from hwt.hdl.types.bitsConst import HBitsConst
from hwt.hdl.types.defs import SLICE
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumConst import HEnumConst
from hwt.hdl.types.sliceConst import HSliceConst
from hwt.hdl.variables import HdlSignalItem
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.serializer.simModel.value import ToHdlAstSimModel_value


class ToHdlAstHwt_value(ToHdlAst_Value):
    NONE = HdlValueId("None")
    SLICE = HdlValueId("SLICE", obj=SLICE)

    def is_suitable_for_const_extract(self, val: HConst):
        # full valid values can be represented as int and do not have any
        # constructor overhead, entirely invalid values can be represented by None
        return not val._is_full_valid() and not isinstance(val._dtype, HEnum)

    def as_hdl_HBitsConst(self, val: HBitsConst):
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

    def as_hdl_HdlSignalItem(self, si: Union[HdlSignalItem, HdlIdDef], declaration=False):
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
            # if isinstance(si, HdlSignalItem) and si._const:
            #    # to allow const cache to extract constants
            #    return self.as_hdl_Value(si._val)
            if si._isUnnamedExpr and si._rtlObjectOrigin is not None:
                return self.as_hdl(si._rtlObjectOrigin)
            else:
                return HdlValueId(si._name, obj=si)

    def as_hdl_HDictConst(self, val):
        return ToHdlAstSimModel_value.as_hdl_HDictConst(self, val)

    def as_hdl_HArrayConst(self, val: HArrayConst):
        if not val.vld_mask:
            return self.NONE
        # else:
        #    if len(val.val) == val._dtype.size:
        #        allValuesSame = True
        #        values = iter(val.val.values())
        #        reference = next(values)
        #         for v in values:
        #             if allValuesSame:
        #                 allValuesSame = isSameHConst(reference, v)
        #             else:
        #                 break
        #        if allValuesSame:
        #            # all values of items in array are same, use generator
        #            # exression
        #            raise NotImplementedError()
        #            return "[%s for _ in range(%d)]" % (self.Value(reference))

        # if value can not be simplified it is required to serialize it item
        # by item
        return self.as_hdl_HDictConst(val.val)

    def as_hdl_HSliceConst(self, val: HSliceConst):
        if val._is_full_valid():
            return HdlOp(
                HdlOpType.DOWNTO, [
                    HdlValueInt(int(val.val.start), None, None),
                    HdlValueInt(int(val.val.stop), None, None)
                ])
        else:
            raise NotImplementedError()
            return "HSliceConst(slice(%s, %s, %s), SLICE, %d)" % (
                self.as_hdl_Value(val.val.start),
                self.as_hdl_Value(val.val.stop),
                self.as_hdl_Value(val.val.step),
                val.vld_mask)

    def as_hdl_HEnumConst(self, val: HEnumConst):
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
