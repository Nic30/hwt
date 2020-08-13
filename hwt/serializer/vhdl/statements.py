from copy import copy

from hdlConvertorAst.hdlAst._statements import HdlStmAssign
from hwt.hdl.assignment import Assignment
from hwt.hdl.block import HdlStatementBlock
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.switchContainer import SwitchContainer
from hwt.hdl.typeShortcuts import hBit
from hwt.hdl.types.bits import Bits
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.sliceVal import SliceVal
from hwt.hdl.value import HValue
from hwt.hdl.variables import SignalItem
from hwt.serializer.exceptions import SerializerException


class ToHdlAstVhdl2008_statements():

    def as_hdl_Assignment(self, a: Assignment):
        _dst = dst = a.dst
        assert isinstance(dst, SignalItem)

        if a.indexes is not None:
            for i in a.indexes:
                if isinstance(i, SliceVal):
                    i = i.__copy__()
                dst = dst[i]

        src_t = a.src._dtype
        dst_t = dst._dtype
        correct = False
        src = a.src
        if dst_t == src_t:
            correct = True
        else:
            src = a.src
            if (isinstance(dst_t, Bits) and isinstance(src_t, Bits)):
                # std_logic <->  std_logic_vector(0 downto 0) auto conversions
                if dst_t.bit_length() == src_t.bit_length() == 1:
                    if dst_t.force_vector and not src_t.force_vector:
                        dst = dst[0]
                        correct = True
                    elif not dst_t.force_vector and src_t.force_vector:
                        src = src[0]
                        correct = True
                    elif src_t == BOOL:
                        src = src._ternary(hBit(1), hBit(0))
                        correct = True
                elif not src_t.strict_width:
                    if isinstance(src, HValue):
                        src = copy(src)
                        if a.indexes:
                            raise NotImplementedError()

                        src._dtype = dst_t
                        correct = True
                    else:
                        raise NotImplementedError()
                        pass

        if correct:
            src = self.as_hdl(src)
            hdl_a = HdlStmAssign(src, self.as_hdl(dst))
            hdl_a.is_blocking = _dst.virtual_only
            return hdl_a

        raise SerializerException(
            "%s = %s  is not valid assignment\n"
            " because types are different (%r; %r) " % 
            (dst, a.src, dst._dtype, a.src._dtype))

    def can_pop_process_wrap(self, stms, hasToBeVhdlProcess):
        if hasToBeVhdlProcess or len(stms) > 1:
            return False
        else:
            assert len(stms) == 1, stms
            return True

    def has_to_be_process(self, proc: HdlStatementBlock):
        for x in proc.statements:
            if isinstance(x, (IfContainer, SwitchContainer)):
                return True
        return False
