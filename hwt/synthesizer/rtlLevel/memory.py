from hwt.hdl.assignment import Assignment
from hwt.hdl.ifContainter import IfContainer
from hwt.hdl.operator import Operator
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.typeCast import toHVal
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlMemoryBase
from hwt.synthesizer.rtlLevel.rtlSignal import RtlSignal, NO_NOPVAL


class RtlSyncSignal(RtlMemoryBase, RtlSignal):
    """
    Syntax sugar,
    every write is made to next signal, "next" is assigned
    to main signal on every clock rising edge
    """

    def __init__(self, ctx, name, var_type, def_val=None, nop_val=NO_NOPVAL):
        """
        :param ~.ctx: context in which is sig. created (instance of RtlNetlist)
        :param ~.name: suggested name
        :param ~.var_type: type of signal
        :param ~.def_val: default value for signal
            (used as def. val in hdl and for reset)
        """
        super().__init__(ctx, name, var_type, def_val)
        if nop_val is NO_NOPVAL:
            nop_val = self
        self.next = RtlSignal(ctx, name + "_next", var_type,
                              nop_val=nop_val)

    def __call__(self, source):
        """
        assign to signal which is next value of this register

        :return: list of assignments
        """
        if isinstance(source, InterfaceBase):
            source = source._sig

        if source is None:
            source = self._dtype.from_py(None)
        else:
            source = toHVal(source)
            source = source._auto_cast(self._dtype)

        a = Assignment(source, self.next)
        return [a, ]

    def _getAssociatedClk(self):
        d = self.singleDriver()
        assert isinstance(d, IfContainer), d
        cond = d.cond.singleDriver()
        assert isinstance(cond, Operator) and cond.operator is AllOps.RISING_EDGE, cond
        return cond.operands[0]

    def _getAssociatedRst(self):
        d = self.singleDriver()
        assert isinstance(d, IfContainer), d
        cond = d.cond.singleDriver()
        assert isinstance(cond, Operator) and cond.operator is AllOps.RISING_EDGE, cond
        assert len(d.ifTrue) == 1
        reset_if = d.ifTrue[0]
        return reset_if.cond
