from hwt.doc_markers import internal


class SignalOps(object):
    """
    Operands for Signal interface,
    These operands are delegated on RtlSignal object for this interface
    """

    def _auto_cast(self, toT):
        return self._sig._auto_cast(toT)

    @internal
    def _convSign(self, signed):
        return self._sig._convSign(signed)

    def _signed(self):
        return self._convSign(True)

    def _unsigned(self):
        return self._convSign(False)

    def _vec(self):
        return self._convSign(None)

    def _reinterpret_cast(self, toT):
        return self._sig._reinterpret_cast(toT)

    # events
    def _onRisingEdge(self):
        return self._sig._onRisingEdge()

    def _onFallingEdge(self):
        return self._sig._onFallingEdge()

    # comparison
    def _isOn(self):
        """
        convert this signal to hBool
        """
        return self._sig._isOn()

    def _eq(self, other):
        """
        Equality operator "==" is not used because it would damage python
        ecosystem
        """
        return self._sig._eq(other)

    def __ne__(self, other):
        """!="""
        return self._sig.__ne__(other)

    def __gt__(self, other):
        """>"""
        return self._sig.__gt__(other)

    def __lt__(self, other):
        """<"""
        return self._sig.__lt__(other)

    def __ge__(self, other):
        """>="""
        return self._sig.__ge__(other)

    def __le__(self, other):
        """<="""
        return self._sig.__le__(other)

    # bitwise
    def __invert__(self):
        """~ operator - logical negation for one bit signals and hBool
           bitwise inversion for wider signals """
        return self._sig.__invert__()

    def __and__(self, other):
        """
        & operator - logical 'and' for one bit signals and hBool
        bitwise and for wider signals
        """
        return self._sig.__and__(other)

    def __xor__(self, other):
        """
        ^ operator - logical '!=' for one bit signals and hBool
        bitwise and for wider signals
        """
        return self._sig.__xor__(other)

    def __or__(self, other):
        """
        | operator - logical 'or' for one bit signals and hBool
        bitwise and for wider signals
        """
        return self._sig.__or__(other)

    # arithmetic
    def __neg__(self):
        "- operator (unary minus)"
        return self._sig.__neg__()

    def __add__(self, other):
        "+ operator"
        return self._sig.__add__(other)

    def __sub__(self, other):
        "- operator"
        return self._sig.__sub__(other)

    def __mul__(self, other):
        "* operator"
        return self._sig.__mul__(other)

    def __pow__(self, other):
        "** operator"
        return self._sig.__pow__(other)

    def __mod__(self, other):
        "** operator"
        return self._sig.__mod__(other)

    def __truediv__(self, other):
        "/ operator - floating point division"
        return self._sig.__truediv__(other)

    def __floordiv__(self, other):
        "// operator - integer division"
        return self._sig.__floordiv__(other)

    def __lshift__(self, other):
        "<< left shift (on fixed number of bits)"
        return self._sig.__lshift__(other)

    def __rshift__(self, other):
        ">> right shift (on fixed number of bits)"
        return self._sig.__lshift__(other)

    # hdl centric
    def _reversed(self):
        """
        reverse bitorder
        """
        # https://stackoverflow.com/questions/27638960/python-reverse-magic-method
        return self._sig._reversed()

    def _concat(self, *others):
        """
        concatenate signals to one big one
        """
        return self._sig._concat(*others)

    def __getitem__(self, key):
        """
        [] operator key can be slice or index
        """
        return self._sig.__getitem__(key)

    def _ternary(self, ifTrue, ifFalse):
        return self._sig._ternary(ifTrue, ifFalse)

    def __call__(self, source):
        """
        connect this signal to driver

        :attention: it is not call of function it is operator of assignment
        :return: list of assignments
        """
        assert self._isAccessible, self
        return self._sig(source)
