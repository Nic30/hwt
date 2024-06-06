from copy import copy
from operator import lshift, rshift

from hwt.doc_markers import internal
from hwt.hdl.operatorDefs import HwtOps, HOperatorDef, CAST_OPS
from hwt.hdl.statements.assignmentContainer import HdlAssignmentContainer
from hwt.hdl.statements.statement import HwtSyntaxError
from hwt.hdl.types.bits import HBits
from hwt.hdl.types.defs import BOOL
from hwt.hdl.types.sliceUtils import slice_to_HSlice
from hwt.hdl.types.typeCast import toHVal
from hwt.mainBases import HwIOBase
from hwt.mainBases import RtlSignalBase
from hwt.synthesizer.exceptions import TypeConversionErr
from hwt.synthesizer.rtlLevel.exceptions import SignalDriverErr
from hwt.synthesizer.vectorUtils import fitTo_t


def getVarCls(signal):
    """
    HValue class for HDL type of signal
    """
    return signal._dtype.getConstCls()


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
    def naryOp(self, operator: HOperatorDef, opCreateDelegate , *otherOps) -> RtlSignalBase:
        """
        Try lookup operator with this parameters in _usedOps
        if not found create new one and stored it in _usedOps

        :param operator: instance of HOperatorDef
        :param opCreateDelegate: function (\\*ops) to create operator
        :param otherOps: other operands (ops = self + otherOps)

        :return: RtlSignal which is result of newly created operator
        """
        indexOfSelfInOperands = 0
        k = (operator, indexOfSelfInOperands, *otherOps)
        used = self._usedOps
        try:
            return used[k]
        except KeyError:
            pass

        o = opCreateDelegate(self, *otherOps)
        # input operands may be type converted,
        # search if this happened, and return always same result signal
        try:
            op_instantiated = (o.origin.operator == operator
                               and o.origin.operands[indexOfSelfInOperands] is self)
        except AttributeError:
            op_instantiated = False

        usedOpsAlias = self._usedOpsAlias
        if op_instantiated:
            # try check real operands and operator which were used after all default type conversions
            k_real = (operator, indexOfSelfInOperands, *o.origin.operands[1:])
            if k != k_real:
                alias = usedOpsAlias[k_real]
                usedOpsAlias[k] = alias
                alias.add(k)
                used[k] = o

        return o

    def __invert__(self):
        try:
            return self.naryOp(HwtOps.NOT, getVarCls(self).__invert__)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _onRisingEdge(self):
        try:
            return self.naryOp(HwtOps.RISING_EDGE, getVarCls(self)._onRisingEdge)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _onFallingEdge(self):
        try:
            return self.naryOp(HwtOps.FALLING_EDGE, getVarCls(self)._onFallingEdge)
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
            return getVarCls(self)._convSign(self, signed)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _signed(self):
        try:
            return getVarCls(self)._signed(self)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _unsigned(self):
        try:
            return getVarCls(self)._unsigned(self)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _vec(self):
        try:
            return getVarCls(self)._vec(self)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # logic
    def __and__(self, other):
        try:
            return self.naryOp(HwtOps.AND, getVarCls(self).__and__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __xor__(self, other):
        try:
            return self.naryOp(HwtOps.XOR, getVarCls(self).__xor__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __or__(self, other):
        try:
            return self.naryOp(HwtOps.OR, getVarCls(self).__or__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __lshift__(self, other):
        try:
            return self.naryOp(lshift, getVarCls(self).__lshift__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __rshift__(self, other):
        try:
            return self.naryOp(rshift, getVarCls(self).__rshift__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # cmp
    def _eq(self, other):
        """
        :attention: __eq__ is not overloaded because it will destroy hashability of object
        """
        try:
            return self.naryOp(HwtOps.EQ, getVarCls(self)._eq, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __ne__(self, other):
        try:
            return self.naryOp(HwtOps.NE, getVarCls(self).__ne__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __ge__(self, other):
        try:
            return self.naryOp(HwtOps.GE, getVarCls(self).__ge__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __gt__(self, other):
        try:
            return self.naryOp(HwtOps.GT, getVarCls(self).__gt__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __lt__(self, other):
        try:
            return self.naryOp(HwtOps.LT, getVarCls(self).__lt__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __le__(self, other):
        try:
            return self.naryOp(HwtOps.LE, getVarCls(self).__le__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    # arithmetic
    def __neg__(self):
        try:
            return self.naryOp(HwtOps.ADD, getVarCls(self).__neg__)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __add__(self, other):
        try:
            return self.naryOp(HwtOps.ADD, getVarCls(self).__add__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __sub__(self, other):
        try:
            return self.naryOp(HwtOps.SUB, getVarCls(self).__sub__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __mul__(self, other):
        try:
            return self.naryOp(HwtOps.MUL, getVarCls(self).__mul__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __mod__(self, other):
        try:
            return self.naryOp(HwtOps.MOD, getVarCls(self).__mod__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __pow__(self, other):
        try:
            return self.naryOp(HwtOps.POW, getVarCls(self).__pow__, other)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __floordiv__(self, divider):
        try:
            t = self._dtype
            return self.naryOp(HwtOps.DIV if not isinstance(t, HBits) else HwtOps.SDIV if t.signed else HwtOps.UDIV, getVarCls(self).__floordiv__, divider)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __getitem__(self, key):
        try:
            if isinstance(key, slice):
                key = slice_to_HSlice(key, self._dtype.bit_length())
            return self.naryOp(HwtOps.INDEX, getVarCls(self).__getitem__, key)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _concat(self, *operands):
        try:
            return self.naryOp(HwtOps.CONCAT, getVarCls(self)._concat, *operands)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def _ternary(self, ifTrue, ifFalse):
        try:
            return self.naryOp(HwtOps.TERNARY, getVarCls(self)._ternary, ifTrue, ifFalse)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    @internal
    def _getIndexCascade(self):
        """
        Find out if this signal is something indexed
        """
        hwIO = self
        indexes = []
        sign_cast_seen = False
        while True:
            try:
                # now self is the result of the index  xxx[xx] <= source
                # get index op
                d = hwIO.singleDriver()
                try:
                    op = d.operator
                except AttributeError:
                    # probably port or statement
                    break

                if op == HwtOps.INDEX:
                    # get signal on which is index applied
                    indexedOn = d.operands[0]
                    if isinstance(indexedOn, RtlSignalBase):
                        hwIO = indexedOn
                        indexes.append(d.operands[1])
                    else:
                        raise HwtSyntaxError(
                            f"can not assign to a static value {indexedOn}")
                elif op in CAST_OPS:
                    sign_cast_seen = True
                    hwIO = d.operands[0]
                else:
                    # the concatenations should have been already resolved before entering of this function
                    raise HwtSyntaxError(
                        f"can not assign to result of operator {d}")

            except SignalDriverErr:
                break

        if not indexes:
            indexes = None
        else:
            indexes.reverse()

        return hwIO, indexes, sign_cast_seen

    def _getDestinationSignalForAssignmentToThis(self):
        """
        :return: a signal which should be used as a destination if assigning to this signal
        """
        return self

    def __call__(self, source,
                 dst_resolve_fn=lambda x: x._getDestinationSignalForAssignmentToThis(),
                 exclude=None,
                 fit=False) -> HdlAssignmentContainer:
        """
        Create assignment to this signal

        :attention: it is not call of function it is operator of assignment
        :return: list of assignments
        """
        assert not self._const, self
        if exclude is not None and (self in exclude or source in exclude):
            return []

        if isinstance(source, HwIOBase):
            assert source._isAccessible, (source, "must be a Signal Interface which is accessible in current scope")
            source = source._sig

        try:
            if source is None:
                requires_type_check = False
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
                if fit:
                    source = fitTo_t(source, self._dtype)
                source = source._auto_cast(self._dtype)
            except TypeConversionErr:
                err = True
            if err:
                raise TypeConversionErr(
                    ("Can not connect %r (of type %r) to %r "
                     "(of type %r) due type incompatibility")
                    % (source, source._dtype, self, self._dtype))
        if self.hidden:
            try:
                d = self.singleDriver()
            except:
                d = None
            operator = getattr(d, "operator", None)
            if operator is not None:
                if operator.allowsAssignTo:
                    if operator == HwtOps.NOT:
                        # instead of assigning to negation we assign the negation
                        return d.operands[0](~source, dst_resolve_fn=dst_resolve_fn, exclude=exclude, fit=fit)
                    elif operator in CAST_OPS:
                        # we need to assert that src and dst type matches, but we do not anything else
                        dst = d.operands[0]
                        src_sign = source._dtype.signed
                        dst_sign = dst._dtype.signed
                        if src_sign == dst_sign:
                            return dst(source)
                        elif dst_sign is None:
                            return dst(source._vec())
                        elif dst_sign:
                            return dst(source._signed())
                        else:
                            return dst(source._unsigned())

                    elif operator == HwtOps.CONCAT:
                        offset = 0
                        res = []
                        # reversed because LSB first
                        for op in reversed(d.operands):
                            w = op._dtype.bit_length()
                            res.append(op(source[w + offset: offset]))
                            offset += w
                        return res
                else:
                    raise AssertionError("Assignment to", self, "is not allowed by operator definition")

        try:
            mainSig, indexCascade, signCastSeen = self._getIndexCascade()
            mainSig = dst_resolve_fn(mainSig)
            if signCastSeen:
                src_sign = source._dtype.signed
                dst_sign = mainSig._dtype.signed
                if src_sign == dst_sign:
                    pass
                elif dst_sign is None:
                    source = source._vec()
                elif dst_sign:
                    source = source._signed()
                else:
                    source = source._unsigned()
            return HdlAssignmentContainer(source, mainSig, indexCascade)
        except Exception as e:
            # simplification of previous exception traceback
            e_simplified = copy(e)
            raise e_simplified

    def __int__(self):
        if not self._const:
            raise TypeError("Int value of signal can not be evaluated"
                            " because it is not constant expression:", self)
        else:
            return int(self._val)

    def __len__(self):
        return getVarCls(self).__len__(self)

    def __bool__(self):
        if not self._const:
            raise TypeError("Bool value of signal can be evaluated"
                            " because it is not constant expression:", self)
        else:
            return bool(self._val)

    def _is_full_valid(self):
        return self._const and self._val._is_full_valid()
