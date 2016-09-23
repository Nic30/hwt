

class SignalOps(object):
    """
    Operands for Signal interface,
    these operands are delegated on RtlSignal object for this interface
    """
    def _convert(self, toT):
        return self._sig._convert(toT)

    # events
    def _onRisingEdge(self):
        return self._sig._onRisingEdge()
    
    def _onFallingEdge(self):
        return self._sig._onFallingEdge()

    def _hasEvent(self):
        return self._sig._hasEvent()
    
    # comparisions
    def _isOn(self):
        """
        convert this signal to hBool
        """
        return self._sig._isOn()

    def _eq(self, other):
        """
        Equality operator "==" is not used because it would damage python ecosystem
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
    

    # bitewise

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
    
    def __add__(self, other):
        return self._sig.__add__(other)
    
    def __sub__(self, other):
        return self._sig.__sub__(other)
    
    def __mul__(self, other):
        return self._sig.__mul__(other)
    
    
    # hdl centric
    def _reversed(self):
        """
        reverse bitorder 
        """
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
    
    
    def __pow__(self, source):
        """
        connect this signal to driver
        @attention: it is not power operator it is assignment
        @return: list of assignments
        """
        return self._sig.__pow__(source)