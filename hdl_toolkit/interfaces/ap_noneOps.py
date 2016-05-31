

class Ap_noneOps(object):
    
    def __invert__(self):
        """~ operator - logical negation for one bit signals and hBool
           bitwise inversion for wider signals """
        return self._sig.__invert__()
    
    def _isOn(self):
        """
        convert this signal to hBool
        """
        return self._sig._isOn()

    def _onRisingEdge(self):
        return self._sig._onRisingEdge()
    
    
    def _eq(self, other):
        """
        Equality operator "==" is not used because it would damage python ecosystem
        """
        return self._sig._eq(other) 
    
    
    # logical ops
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
    
    
    def _concat(self, *operands):
        """
        concatenate signals to one big one. works like & in vhdl
        """
        return self._sig._concat(*operands)
    
    def __getitem__(self, key):
        """
        [] operator key can be slice or index
        """
        return self._sig.__getitem__(key)
    
    def _ternary(self, ifTrue, ifFalse):
        return self._sig._ternary(ifTrue, ifFalse)
    
    def _slice(self, index):
        """
        functional form of __getitem__
        """
        return self._sig._slice(index)
    
    def _assignFrom(self, source):
        """
        connect this signal to driver
        """
        return self._sig._assignFrom(source)
