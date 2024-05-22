from typing import Union

from hdlConvertorAst.hdlAst._expr import HdlValueId, HdlOp, HdlOpType
from hdlConvertorAst.to.hdlUtils import bit_string
from hdlConvertorAst.to.verilog.constants import SIGNAL_TYPE
from hdlConvertorAst.translate.common.name_scope import LanguageKeyword
from hdlConvertorAst.translate.verilog_to_basic_hdl_sim_model.utils import hdl_call, \
    hdl_getattr
from hwt.hdl.const import HConst
from hwt.hdl.operator import HOperatorNode
from hwt.hdl.operatorDefs import HwtOps
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import SLICE
from hwt.hdl.types.enumConst import HEnumConst
from hwt.hdl.variables import HdlSignalItem
from hwt.pyUtils.typingFuture import override
from hwt.serializer.generic.value import ToHdlAst_Value
from hwt.serializer.hwt.ops import ToHdlAstHwt_ops
from hwt.serializer.systemC.utils import systemCTypeOfSig
from hwt.serializer.verilog.context import SignalTypeSwap
from hwt.serializer.verilog.ops import ToHdlAstVerilog_ops
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal


class ToHdlAstSystemC_expr(ToHdlAst_Value):
    static_cast = HdlValueId("static_cast", obj=LanguageKeyword())
    op_transl_dict = ToHdlAstVerilog_ops.op_transl_dict

    def as_hdl_Value(self, v):
        if isinstance(v, tuple):
            return tuple((self.as_hdl(o2) for o2 in v))
        return super(ToHdlAstSystemC_expr, self).as_hdl_Value(v)

    def as_hdl_operand(self, operand: Union[RtlSignal, HConst], i: int,
                       operator: HOperatorNode):
        return self.as_hdl(operand)

    def as_hdl_HOperatorNode(self, op: HOperatorNode):
        ops = op.operands
        o = op.operator

        if o == HwtOps.INDEX:
            assert len(ops) == 2
            o0, o1 = ops
            if o1._dtype == SLICE:
                # index to .range(x, y)
                o0_hdl = self.as_hdl_operand(o0, 0, op)
                o0_hdl = hdl_getattr(o0_hdl, "range")
                return hdl_call(o0_hdl, [self.as_hdl_Value(o1.val.start),
                                         self.as_hdl_Value(o1.val.stop)])
            else:
                return ToHdlAstVerilog_ops.as_hdl_HOperatorNode(self, op)
        elif o in ToHdlAstHwt_ops._cast_ops:
            assert len(ops) == 1, ops
            t = self.as_hdl_HdlType(op.result._dtype)
            return hdl_call(
                HdlOp(HdlOpType.PARAMETRIZATION, [self.static_cast, t]),
                [self.as_hdl_Value(ops[0]), ])
        elif o == HwtOps.CONCAT:
            isNew, o = self.tmpVars.create_var_cached("tmpConcat_",
                                                      op.result._dtype,
                                                      postponed_init=True,
                                                      extra_args=(HwtOps.CONCAT, op.result))
            if isNew:
                o.drivers.append(HdlAssignmentContainer(op, o, virtual_only=True))
                self.tmpVars.finish_var_init(o)

            return self.as_hdl(o)
        else:
            return ToHdlAstVerilog_ops.as_hdl_HOperatorNode(self, op)

    @override
    def as_hdl_HdlSignalItem(self, si: HdlSignalItem, declaration=False):
        if declaration:
            sigType = systemCTypeOfSig(si)
            with SignalTypeSwap(self, sigType):
                return ToHdlAst_Value.as_hdl_HdlSignalItem(self, si, declaration=True)
        else:
            if si.hidden and si.origin is not None:
                return self.as_hdl(si.origin)
            else:
                sigType = systemCTypeOfSig(si)
                _si = HdlValueId(si._name, obj=si)
                if self._in_sensitivity_list or self._is_target or sigType is SIGNAL_TYPE.REG:
                    return _si
                else:
                    return hdl_call(hdl_getattr(_si, "read"), [])

    def as_hdl_HBitsConst(self, val):
        t = val._dtype
        w = t.bit_length()
        _v = bit_string(val.val, w, val.vld_mask)
        t = self.as_hdl_HdlType_bits(HBits(w, signed=t.signed))
        return hdl_call(t, [_v, ])

    def as_hdl_HEnumConst(self, val: HEnumConst):
        i = val._dtype._allValues.index(val.val)
        assert i >= 0
        return self.as_hdl_int(i)

    def as_hdl_HArrayConst(self, val):
        return [self.as_hdl_Value(v) for v in val]
