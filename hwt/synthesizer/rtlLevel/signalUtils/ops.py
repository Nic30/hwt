from copy import copy
from operator import lshift, rshift

from hwt.doc_markers import internal
from hwt.hdl.assignment import Assignment
from hwt.hdl.operatorDefs import AllOps
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.sliceUtils import slice_to_SLICE
from hwt.hdl.types.typeCast import toHVal
from hwt.synthesizer.exceptions import TypeConversionErr
from hwt.synthesizer.interfaceLevel.mainBases import InterfaceBase
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.synthesizer.rtlLevel.signalUtils.exceptions import SignalDriverErr


def tv(signal):
    """
    HValue class for type of signal
    """
    return signal._dtype.getValueCls()


class RtlSignalOps():
    """
    Definitions of operators and other operator functions for RtlSignal

    :ivar ~._usedOps: cache for expressions with this signal
    """

    def _auto_cast(self, toT):
        try:
            return self._dtype.auto_cast(self, toT)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _reinterpret_cast(self, toT):
        try:
            return self._dtype.reinterpret_cast(self, toT)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    @internal
    def naryOp(self, operator, opCreateDelegate, *otherOps) -> RtlSignalBase:
        """
        Try lookup operator with this parameters in _usedOps
        if not found create new one and soter it in _usedOps

        :param operator: instance of OpDefinition
        :param opCreateDelegate: function (\*ops) to create operator
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
            op_instantiated = (o.origin.operator == operator
                               and o.origin.operands[0] is self)
        except AttributeError:
            op_instantiated = False

        if op_instantiated:
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
        try:
            return self.naryOp(AllOps.NOT, tv(self).__invert__)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _onRisingEdge(self):
        try:
            return self.naryOp(AllOps.RISING_EDGE, tv(self)._onRisingEdge)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _onFallingEdge(self):
        try:
            return self.naryOp(AllOps.FALLING_EDGE, tv(self)._onFallingEdge)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _isOn(self):
        try:
            return self._auto_cast(BOOL)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # conversions
    def _convSign(self, signed):
        try:
            return tv(self)._convSign(self, signed)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _signed(self):
        try:
            return tv(self)._signed(self)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _unsigned(self):
        try:
            return tv(self)._unsigned(self)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _vec(self):
        try:
            return tv(self)._vec(self)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # logic
    def __and__(self, other):
        try:
            return self.naryOp(AllOps.AND, tv(self).__and__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __xor__(self, other):
        try:
            return self.naryOp(AllOps.XOR, tv(self).__xor__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __or__(self, other):
        try:
            return self.naryOp(AllOps.OR, tv(self).__or__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __lshift__(self, other):
        try:
            return self.naryOp(lshift, tv(self).__lshift__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __rshift__(self, other):
        try:
            return self.naryOp(rshift, tv(self).__rshift__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # cmp
    def _eq(self, other):
        """
        __eq__ is not overloaded because it will destroy hashability of object
        """
        try:
            return self.naryOp(AllOps.EQ, tv(self)._eq, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __ne__(self, other):
        try:
            return self.naryOp(AllOps.NE, tv(self).__ne__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __ge__(self, other):
        try:
            return self.naryOp(AllOps.GE, tv(self).__ge__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __gt__(self, other):
        try:
            return self.naryOp(AllOps.GT, tv(self).__gt__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __lt__(self, other):
        try:
            return self.naryOp(AllOps.LT, tv(self).__lt__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __le__(self, other):
        try:
            return self.naryOp(AllOps.LE, tv(self).__le__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # arithmetic
    def __neg__(self):
        try:
            return self.naryOp(AllOps.ADD, tv(self).__neg__)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __add__(self, other):
        try:
            return self.naryOp(AllOps.ADD, tv(self).__add__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __sub__(self, other):
        try:
            return self.naryOp(AllOps.SUB, tv(self).__sub__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __mul__(self, other):
        try:
            return self.naryOp(AllOps.MUL, tv(self).__mul__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __mod__(self, other):
        try:
            return self.naryOp(AllOps.MOD, tv(self).__mod__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __pow__(self, other):
        try:
            return self.naryOp(AllOps.POW, tv(self).__pow__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __floordiv__(self, divider):
        try:
            return self.naryOp(AllOps.DIV, tv(self).__floordiv__, divider)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __getitem__(self, key):
        try:
            if isinstance(key, slice):
                key = slice_to_SLICE(key, self._dtype.bit_length())
            return self.naryOp(AllOps.INDEX, tv(self).__getitem__, key)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _concat(self, *operands):
        try:
            return self.naryOp(AllOps.CONCAT, tv(self)._concat, *operands)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _ternary(self, ifTrue, ifFalse):
        try:
            return self.naryOp(AllOps.TERNARY, tv(self)._ternary, ifTrue, ifFalse)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

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
            except SignalDriverErr:
                break

        if not indexes:
            indexes = None
        else:
            indexes.reverse()

        return intf, indexes

    def __call__(self, source) -> Assignment:
        """
        Create assignment to this signal

        :attention: it is not call of function it is operator of assignment
        :return: list of assignments
        """
        assert not self._const, self
        if isinstance(source, InterfaceBase):
            assert source._isAccessible, source
            source = source._sig

        try:
            requires_type_check = False
            if source is None:
                source = self._dtype.from_py(None)
            else:
                requires_type_check = True
                source = toHVal(source, suggestedType=self._dtype)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

        if requires_type_check:
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
        try:
            mainSig, indexCascade = self._getIndexCascade()
            return Assignment(source, mainSig, indexCascade)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

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
