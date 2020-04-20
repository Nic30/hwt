from hdlConvertor.hdlAst._expr import HdlIntValue, HdlCall, HdlBuiltinFn,\
    HdlName, HdlDirection
from hdlConvertor.translate._verilog_to_basic_hdl_sim_model.utils import hdl_getattr,\
    hdl_call
from hwt.hdl.statement import isSameHVal
from hwt.hdl.types.arrayVal import HArrayVal
from hwt.hdl.types.bitsVal import BitsVal
from hwt.hdl.types.defs import SLICE
from hwt.hdl.types.enum import HEnum
from hwt.hdl.types.enumVal import HEnumVal
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.variables import SignalItem
from hwt.serializer.generic.indent import getIndent
from hwt.serializer.generic.value import ToHdlAst_Value
from hdlConvertor.hdlAst._defs import HdlVariableDef
from typing import Union
from hwt.serializer.simModel.serializer import ToHdlAstSimModel
from hwt.serializer.simModel.value import ToHdlAstSimModel_value


class ToHdlAstHwt_value(ToHdlAst_Value):
    NONE = HdlName("None")
    SLICE = HdlName("SLICE", obj=SLICE)

    def as_hdl_BitsVal(self, val: BitsVal):
        isFullVld = val._is_full_valid()
        if not self._valueWidthRequired:
            if isFullVld:
                return HdlIntValue(val.val, None, 16)
            elif val.vld_mask == 0:
                return self.NONE

        t = self.as_hdl_HdlType_bits(val._dtype, declaration=False)
        c = hdl_getattr(t, "from_py")
        args = [HdlIntValue(val.val, None, 16), ]
        if not isFullVld:
            args.append(HdlIntValue(val.vld_mask, None, 16))

        return hdl_call(c, args)

    def as_hdl_SignalItem(self, si: Union[SignalItem, HdlVariableDef], declaration=False):
        if declaration:
            if isinstance(si, HdlVariableDef):
                si.type = self.as_hdl_HdlType(si.type)
                if si.value is not None:
                    si.value = self.as_hdl_Value(si.value)
                return si
            else:
                raise NotImplementedError()
        else:
            if isinstance(si, SignalItem) and si._const:
                # to allow const cache to extract constants
                return self.as_hdl_Value(si._val)
            elif si.hidden and hasattr(si, "origin"):
                return self.as_hdl(si.origin)
            else:
                return HdlName(si.name, obj=si)

    def Value_try_extract_as_const(self, val):
        # try to extract value as constant
        try:
            consGetter = self.constCache.getConstName
        except AttributeError:
            consGetter = None

        if consGetter and not val._is_full_valid() and not isinstance(val._dtype, HEnum):
            return consGetter(val)

    def as_hdl_DictVal(self, val):
        return ToHdlAstSimModel_value.as_hdl_DictVal(self, val)

    def as_hdl_HArrayVal(self, val: HArrayVal):
        if not val.vld_mask:
            return self.NONE
        else:
            if len(val.val) == val._dtype.size:
                allValuesSame = True
                values = iter(val.val.values())
                reference = next(values)
                for v in values:
                    if allValuesSame:
                        allValuesSame = isSameHVal(reference, v)
                    else:
                        break
                if allValuesSame:
                    # all values of items in array are same, use generator
                    # exression
                    raise NotImplementedError()
                    return "[%s for _ in range(%d)]" % (self.Value(reference))

        # if value can not be simplified it is required to serialize it item
        # by item
        return self.as_hdl_DictVal(val.val)

    def as_hdl_SliceVal(self, val: SliceVal):
        if val._is_full_valid():
            return HdlCall(
                HdlBuiltinFn.DOWNTO, [
                    HdlIntValue(int(val.val.start), None, None),
                    HdlIntValue(int(val.val.stop), None, None)
                ])
        else:
            raise NotImplementedError()
            return "SliceVal(slice(%s, %s, %s), SLICE, %d)" % (
                self.as_hdl_Value(val.val.start),
                self.as_hdl_Value(val.val.stop),
                self.as_hdl_Value(val.val.step),
                val.vld_mask)

    def as_hdl_HEnumVal(self, t, val: HEnumVal):
        return hdl_getattr(HdlName(t.name, obj=t), val.val)
