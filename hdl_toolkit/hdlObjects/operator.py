from copy import deepcopy
from hdl_toolkit.synthetisator.rtlLevel.rtlSignal import RtlSignal, RtlSignalBase 
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.hdlObjects.function import Function
from hdl_toolkit.hdlObjects.operatorDefs import AllOps
from hdl_toolkit.synthetisator.rtlLevel.mainBases import RtlMemoryBase

class InvalidOperandExc(Exception):
    pass

class Operator():
    """
    Class of operator in expression tree
    @ivar ops: list of operands
    @ivar evalFn: function to evaluate this operator
    @ivar operator: OpDefinition instance 
    @ivar result: result signal of this operator
    @ivar __reversed: used in operators which can change direction of data-flow, for example indexing,
                this is reference on same operator with reversed direction
    """
    def __init__(self, operator, operands):
        self.ops = list(operands)
        self.operator = operator
        self.result = None
        self._isDriver = True
        self._reversed = None
        
        
    def asDrived(self):
        """
        Used in index (operators which can change data-flow direction in process of building netlist)
        xx[x] = result vs result = xx[x]

        @return: operator variant which is driven by result
        
        - drivers/endpoints for netlist walking
        
        - index created as driven by result by default  (result = xx[x])
        - index should be reversed on assignment to it  (-> xx[x] = result )
        - operators are cached for each signal          
        - reversing operation has to keep other uses of this op as they are
        - sync signal should on reverse replace itself with next signal 
        
        
        """
        if not self._isDriver:
            return self
        
        
        
        if self._reversed is None:
            # create op with changed direction (result -> ops)
            # result = indexedOn[xxx]  to indexedOn[xxx] = result
            indexedOn = self.ops[0]
            if isinstance(indexedOn, RtlMemoryBase): # [TODO] this logic should be in RtlMemory
                indexedOn = indexedOn.next
                
            index = self.ops[1]
            
            rev = self._reversed = Operator(self.operator, [indexedOn, index])
            rev._isDriver = False
            rev._reversed = self
            
            # wrap it with result signal
            out = RtlSignal(None, self.result._dtype)
            out.endpoints.append(rev)
            out.origin = rev
            rev.result = out
            rev.registerSignals([indexedOn])
            
            
        return self._reversed
        
    
    def asDriver(self):
        """
        Used in index (operators which can change data-flow direction in process of building netlist)
        xx[x] = result vs result = xx[x]
        
        @return: operator variant which is driving result
        """
        if self._isDriver:
            return self
        
        if self._reversed is None:
            raise Exception("Reversed op should have been already instantiated")
            # because all operators should be drivers by default
        else:
            raise self._reversed
        
            
    def registerSignals(self, outputs=[]):
        """
        Register potential signals to drivers/endpoints
        """
        for o in self.ops:
            if isinstance(o, RtlSignalBase):
                if o in outputs:
                    o.drivers.append(self)
                else:
                    o.endpoints.append(self)
            elif isinstance(o, (Value, Function)):
                pass
            else:
                raise NotImplementedError("Operator operands can be only signal or values got:%s" % repr(o))
                
    
    def simEval(self, simulator):
        """
        Recursively statistically evaluate result of this operator
        if signal has not set hidden flag do not reevaluate it
        """
        if self.operator == AllOps.INDEX and self in self.result.endpoints:
            # this should not be evaluated because it is part of assignments like xx[xx] =
            # this will be evaluated when assignment is active
            raise NotImplementedError("propagate index on other side %s" % repr(self))
        else:
            for o in self.ops:
                if isinstance(o, RtlSignalBase) and o.hidden:
                    o.simEval(simulator)
            self.result._val = self.evalFn(simulator=simulator)
            
    def staticEval(self):
        """
        Recursively statistically evaluate result of this operator
        """
        if self.operator == AllOps.INDEX and self in self.result.endpoints:
            raise NotImplementedError("propagate index on other side")
        else:
            for o in self.ops:
                o.staticEval()
            self.result._val = self.evalFn()
            
    def evalFn(self, simulator=None):
        """
        Syntax sugar
        """
        return self.operator.eval(self, simulator=simulator)
    
    def __eq__(self, other):
        return self is other or (
             type(self) == type(other) 
            and self.operator == other.operator \
            and self.ops == other.ops)
    
    @staticmethod
    def withRes(opDef, operands, resT, outputs=[]):
        """
        Create operator with result signal
        """
        op = Operator(opDef, operands)
        out = RtlSignal(None, resT)
        out.drivers.append(op)
        out.origin = op
        op.result = out
        op.registerSignals(outputs)
        
        return out
    
    def __deepcopy__(self, memo=None):
        try:
            return memo[self]
        except KeyError:
            o = Operator(None, [])
            memo[id(self)] = o
            for k, v in self.__dict__.items():
                setattr(o, k, deepcopy(v, memo))

            return o
                
    def __hash__(self):
        return hash((self.operator, frozenset(self.ops)))
    
        
    def __repr__(self):
        return "<%s operator:%s, ops:%s>" % (self.__class__.__name__,
                                             repr(self.operator), repr(self.ops))
