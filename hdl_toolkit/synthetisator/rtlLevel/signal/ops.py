from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.hdlObjects.types.defs import BOOL
from hdl_toolkit.hdlObjects.types.typeCast import toHVal
from hdl_toolkit.hdlObjects.assignment import Assignment
from hdl_toolkit.synthetisator.rtlLevel.signal.exceptions import MultipleDriversExc
from hdl_toolkit.hdlObjects.variables import SignalItem
from hdl_toolkit.hdlObjects.value import Value

def tv(signal):
    """
    Value class for type of signal
    """
    return signal._dtype.getValueCls()

class SignalOps():
    def _convert(self, toT):
        return tv(self)._convert(self, toT)
    
    def naryOp(self, operator, opCreateDelegate, *otherOps):
        k = (operator, *otherOps)
        try:
            return self._usedOps[k]
        except KeyError:
            o = opCreateDelegate(self, *otherOps)
            self._usedOps[k] = o
            return o  
        
        return o
    
    def __invert__(self):
        return self.naryOp(AllOps.NOT, tv(self).__invert__)
        
    def _onRisingEdge(self):
        return self.naryOp(AllOps.RISING_EDGE, tv(self)._onRisingEdge)
    
    def _hasEvent(self):
        raise self.naryOp(AllOps.EVENT, tv(self)._hasEvent)
    
    def _isOn(self):
        return self._dtype.convert(self, BOOL)
        
    def __and__(self, other):
        return self.naryOp(AllOps.AND_LOG, tv(self).__and__, other)
    
    def __xor__(self, other):
        return self.naryOp(AllOps.XOR, tv(self).__xor__, other)

    def __or__(self, other):
        return self.naryOp(AllOps.OR_LOG, tv(self).__or__, other)

    def _eq(self, other):
        """__eq__ is not overloaded because it will destroy hashability of object"""
        return self.naryOp(AllOps.EQ, tv(self)._eq, other)

    def __ne__(self, other):
        return self.naryOp(AllOps.NEQ, tv(self).__ne__, other)
    
    def __add__(self, other):
        return self.naryOp(AllOps.ADD, tv(self).__add__, other)
    
    def __sub__(self, other):
        return self.naryOp(AllOps.SUB, tv(self).__sub__, other)
    
    def __mul__(self, other):
        return self.naryOp(AllOps.MUL, tv(self).__mul__, other)

    def __floordiv__(self, divider):
        return self.naryOp(AllOps.DIV, tv(self).__floordiv__, divider)
    
    def _downto(self, to):
        return self.naryOp(AllOps.DOWNTO, tv(self)._downto, to)
    
    def __getitem__(self, key):
        return self.binOp(AllOps.INDEX, tv(self).__getitem__, key)

    def _concat(self, *operands):
        return self.naryOp(AllOps.CONCAT, tv(self)._concat, *operands)
    
    def _ternary(self, ifTrue, ifFalse):
        return self.naryOp(AllOps.TERNARY, tv(self)._ternary, ifTrue, ifFalse)
    
    def _assignFrom(self, source):
        from hdl_toolkit.hdlObjects.operator import Operator
        
        source = toHVal(source)
        a = Assignment(source, self)
        a.cond = set()
        
        try:
            # now I am result of the index  self[xx] <= source
            # get index op
            d = self.singleDriver()
            if isinstance(d, Operator) and d.operator == AllOps.INDEX:
                # get singla on which is signal applied
                indexedOn = d.ops[0]
                if isinstance(indexedOn, SignalItem):
                    # change direction of index for me and for indexed on
                    # print(d, 'to driver of', indexedOn)
                    indexedOn.endpoints.remove(d)
                    indexedOn.drivers.append(d)
                     
                    # print(d, "to endpoint of")    
                    self.drivers.remove(d)
                    self.endpoints.append(d)
        except MultipleDriversExc:
            pass
        
        self.drivers.append(a)
        if not isinstance(source, Value):
            source.endpoints.append(a)
        
        return a
    
