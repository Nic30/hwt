from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.sliceUtils import slice_to_SLICE
from hwt.hdl.types.typeCast import toHVal
from hwt.synthesizer.exceptions import TypeConversionErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import MultipleDriversErr, \
    NoDriverErr


def tv(signal):
    """
    Value class for type of signal
    """
    return signal._dtype.getValueCls()


class RtlSignalOps():
    """
    Definitions of operators and other operator functions for RtlSignal

    :ivar _usedOps: cache for expressions with this signal
    """

    def _auto_cast(self, toT):
        return self._dtype.auto_cast(self, toT)

    def _reinterpret_cast(self, toT):
        return self._dtype.reinterpret_cast(self, toT)

    @internal
    def naryOp(self, operator, opCreateDelegate, *otherOps) -> RtlSignalBase:
        """
        Try lookup operator with this parameters in _usedOps
        if not found create new one and soter it in _usedOps

        :param operator: instance of OpDefinition
        :param opCreateDelegate: function (*ops) to create operator
        :param otherOps: other operands (ops = self + otherOps)

        :return: RtlSignal which is result of newly created operator
        """
        k = (operator, *otherOps)
        used = self._usedOps
        try:
            return used[k]
        except KeyError:
            pass

        o = opCreateDelegate(self, *otherOps)

        # input operads may be type converted,
        # search if this happend, and return always same result signal
        try:
            op_instanciated = (o.origin.operator == operator
                               and o.origin.operands[0] is self)
        except AttributeError:
            op_instanciated = False

        if op_instanciated:
            k_real = (operator, *o.origin.operands[1:])
            real_o = used.get(k_real, None)
            if real_o is not None and real_o is not o:
                # destroy newly created operator and result, because it is same
                # as the signal for some existing operator with equvavelnt value
                # (and maybe possibly slightly different type)
                ctx = self.ctx
                if ctx is not None:
                    ctx.signals.remove(o)

                op = o.origin
                o.origin = None
                o.drivers.clear()
                for inp in op.operands:
                    if isinstance(inp, RtlSignalBase):
                        inp.endpoints.remove(op)

                o = real_o
            else:
                used[k_real] = o

        used[k] = o

        return o

    def __invert__(self):
        return self.naryOp(AllOps.NOT, tv(self).__invert__)

    def _onRisingEdge(self):
        return self.naryOp(AllOps.RISING_EDGE, tv(self)._onRisingEdge)

    def _onFallingEdge(self):
        return self.naryOp(AllOps.FALLING_EDGE, tv(self)._onFallingEdge)

    def _isOn(self):
        return self._auto_cast(BOOL)

    # conversions
    def _convSign(self, signed):
        return tv(self)._convSign(self, signed)

    def _signed(self):
        return tv(self)._signed(self)

    def _unsigned(self):
        return tv(self)._unsigned(self)

    def _vec(self):
        return tv(self)._vec(self)

    # logic
    def __and__(self, other):
        return self.naryOp(AllOps.AND, tv(self).__and__, other)

    def __xor__(self, other):
        return self.naryOp(AllOps.XOR, tv(self).__xor__, other)

    def __or__(self, other):
        return self.naryOp(AllOps.OR, tv(self).__or__, other)

    # cmp
    def _eq(self, other):
        """
        __eq__ is not overloaded because it will destroy hashability of object
        """
        return self.naryOp(AllOps.EQ, tv(self)._eq, other)

    def __ne__(self, other):
        return self.naryOp(AllOps.NEQ, tv(self).__ne__, other)

    def __ge__(self, other):
        return self.naryOp(AllOps.GE, tv(self).__ge__, other)

    def __gt__(self, other):
        return self.naryOp(AllOps.GT, tv(self).__gt__, other)

    def __lt__(self, other):
        return self.naryOp(AllOps.LT, tv(self).__lt__, other)

    def __le__(self, other):
        return self.naryOp(AllOps.LE, tv(self).__le__, other)

    # arithmetic
    def __add__(self, other):
        return self.naryOp(AllOps.ADD, tv(self).__add__, other)

    def __sub__(self, other):
        return self.naryOp(AllOps.SUB, tv(self).__sub__, other)

    def __mul__(self, other):
        return self.naryOp(AllOps.MUL, tv(self).__mul__, other)

    def __floordiv__(self, divider):
        return self.naryOp(AllOps.DIV, tv(self).__floordiv__, divider)

    def __getitem__(self, key):
        if isinstance(key, slice):
            key = slice_to_SLICE(key, self._dtype.bit_length())
        return self.naryOp(AllOps.INDEX, tv(self).__getitem__, key)

    def _concat(self, *operands):
        return self.naryOp(AllOps.CONCAT, tv(self)._concat, *operands)

    def _ternary(self, ifTrue, ifFalse):
        return self.naryOp(AllOps.TERNARY, tv(self)._ternary, ifTrue, ifFalse)

    @internal
    def _getIndexCascade(self):
        """
        Find out if this signal is something indexed
        """
        intf = self
        indexes = []
        while True:
            try:
                # now I am result of the index  xxx[xx] <= source
                # get index op
                d = intf.singleDriver()
                try:
                    op = d.operator
                except AttributeError:
                    break

                if op == AllOps.INDEX:
                    # get signal on which is index applied
                    indexedOn = d.operands[0]
                    if isinstance(indexedOn, RtlSignalBase):
                        intf = indexedOn
                        indexes.append(d.operands[1])
                    else:
                        raise Exception(
                            "can not drive static value %r" % indexedOn)
            except (MultipleDriversErr, NoDriverErr):
                break

        if not indexes:
            indexes = None

        return intf, indexes

    def __call__(self, source) -> Assignment:
        """
        Create assignment to this signal

        :attention: it is not call of function it is operator of assignment
        :return: list of assignments
        """
        assert not self._const, self
        if isinstance(source, InterfaceBase):
            assert source._isAccessible
            source = source._sig

        if source is None:
            source = self._dtype.from_py(None)
        else:
            source = toHVal(source, suggestedType=self._dtype)
            err = False
            try:
                source = source._auto_cast(self._dtype)
            except TypeConversionErr:
                err = True
            if err:
                raise TypeConversionErr(
                    ("Can not connect %r (of type %r) to %r "
                     "(of type %r) due type incompatibility")
                    % (source, source._dtype, self, self._dtype))

        mainSig, indexCascade = self._getIndexCascade()
        return Assignment(source, mainSig, indexCascade)

    def __int__(self):
        if not self._const:
            raise TypeError("Int value of signal can be evaluated"
                            " because it is not constant expression:", self)
        else:
            return int(self._val)

    def __bool__(self):
        if not self._const:
            raise TypeError("Bool value of signal can be evaluated"
                            " because it is not constant expression:", self)
        else:
            return bool(self._val)

    def _is_full_valid(self):
        return self._const and self._val._is_full_valid()
