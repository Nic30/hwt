from hdl_toolkit.hdlObjects.types import HdlType
from hdl_toolkit.hdlObjects.typeOps import TypeOps
from hdl_toolkit.hdlObjects.specialValues import Unconstrained
from hdl_toolkit.hdlObjects.value import Value
from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.synthetisator.exceptions import TypeConversionErr

# [TODO] split to separate file for each type type, cleanup types/typeOps

class Boolean(HdlType):
    def __init__(self):
        super(Boolean, self).__init__()
        self.name = 'boolean'
    
    def valAsVhdl(self, val, serializer):
        return str(bool(val.val))
    
    def convert(self, sigOrVal, toType):
        if sigOrVal._dtype == toType:
            return sigOrVal
        elif toType == BIT:
            if isinstance(sigOrVal, Value):
                pass
            else:
                return sigOrVal._ternary(Value.fromPyVal(1, BIT), Value.fromPyVal(0, BIT))
            
        return super(Boolean, self).convert(sigOrVal, toType)
    
    class Ops(TypeOps):
        @classmethod
        def fromPy(cls, val, typeObj):
            """
            @param val: value of python type bool or None
            @param typeObj: instance of HdlType
            """
            vld = int(val is not None)
            if not vld:
                val = False
            return cls(bool(val), typeObj, vld)
                
        def _eq(self, other):
            """return abs(w.val[0].val - w.val[1].val) + 1
        
            @attention: ignores eventMask
            """
            self._otherCheck(other)
    
            eq = self.val == other.val \
                and self.vldMask == other.vldMask == 1
            
            vldMask = int(self.vldMask == other.vldMask == 1)
            evMask = self.eventMask | other.eventMask
            return self.__class__(eq, BOOL, vldMask, eventMask=evMask)

        def __invert__(self):
            v = self.clone()
            v.val = not v.val
            return v
    
        # logic
        def __and__(self, other):
            self._otherCheck(other)
            # [VHDL-BUG-LIKE] X and 0 should be 0 now is X (in vhdl is now this function correct)
            v = self.val and other.val
            return self.__class__(v, BOOL,
                    self.vldMask & other.vldMask,
                    self.eventMask | other.eventMask)
            
        def __or__(self, other):
            self._otherCheck(other)
            # [VHDL-BUG-LIKE] X or 1 should be 1 now is X (in vhdl is now this function correct) 
            v = bool(self.val) or bool(other.val)
            return self.__class__(v, BOOL,
                    self.vldMask & other.vldMask,
                    self.eventMask | other.eventMask)
    
        def __bool__(self):
            return bool(self.val and self.vldMask)

#    class ValueCls(Value, Ops):
#        pass


# [TODO] from some reason ValueCls in Boolean can not be serialized by dill, 
# other classes seems to work
class Boolean_ValueCls(Value, Boolean.Ops):
    pass
Boolean.ValueCls = Boolean_ValueCls


class Integer(HdlType):
    
    def __init__(self):
        super(Integer, self).__init__()
        self.name = 'integer'

    def valAsVhdl(self, val, serializer):
        return str(int(val.val))
    
    def convert(self, sigOrVal, toType):
        if sigOrVal._dtype == toType:
            return sigOrVal
        elif toType == PINT:
            if isinstance(sigOrVal, Value):
                v = sigOrVal.clone()
                assert(v.val > 0)
                v._dtype = PINT
                return v
        elif toType == UINT:
            if isinstance(sigOrVal, Value):
                v = sigOrVal.clone()
                assert(v.val >= 0)
                v._dtype = UINT
                return v
        elif toType == INT:
            if isinstance(sigOrVal, Value):
                v = sigOrVal.clone()
                v._dtype = INT
                return v
            else:
                return sigOrVal
        elif toType == BIT:
            if isinstance(sigOrVal, Value):
                _v = sigOrVal.val 
                assert(_v == 1 or _v == 0)
                v = sigOrVal.clone()
                v._dtype = BIT
                return v
            else:
                return sigOrVal
        elif isinstance(toType, Std_logic_vector):
            # [TODO] this code is dangerous whole type conversion system needs to be separate from types
            if hasattr(toType, "getBitCnt"):
                w = toType.getBitCnt()
            else:
                w = None
            if isinstance(sigOrVal, Value):
                v = sigOrVal.clone()
                v._dtype = toType
                if w is None:
                    v.vldMask = -1 if v.vldMask else 0
                    v.eventMask = -1 if v.eventMask else 0 
                else:
                    m = Bitmask.mask(w)
                    v.vldMask = m if v.vldMask else 0
                    v.eventMask = m if v.eventMask else 0 
                return v
                
        return super(Integer, self).convert(sigOrVal, toType)

        
    class Ops(TypeOps):
        """
        @ivar vldMask: can be only 0 or 1
        @ivar eventMask: can be only 0 or 1
        """
        @classmethod
        def fromPy(cls, val, typeObj):
            """
            @param val: value of python type int or None
            @param typeObj: instance of HdlType
            """
            vld = int(val is not None)
            if not vld:
                val = 0
            assert(isinstance(val, int))
            
            return cls(int(val), typeObj, vld)
        def __int__(self):
            if self.vldMask:
                return self.val
            else:
                return None
            
        def _eq(self, other):
            self._otherCheck(other)
            vld = self.vldMask and other.vldMask
            eq = self.val == other.val and vld
            ev = self.eventMask or other.eventMask

            vCls = BOOL.ValueCls
            
            return vCls(eq, BOOL, vld, eventMask=ev)
        
        def __neg__(self):
            v = self.clone()
            v.val = -self.val 
            return v
        
        def __add__(self, other):
            self._otherCheck(other)
            v = self.val + other.val
            vldMask = int(self.vldMask and other.vldMask)
            eventMask = int(self.eventMask or other.eventMask)

            return self.__class__(v, INT, vldMask, eventMask)
            
        def __sub__(self, other):
            return self +(-other)
        
        def __mul__(self, other):
            self._otherCheck(other)
            val = self.val * other.val
            vldMask = int(self.vldMask and other.vldMask)
            eventMask = int(self.eventMask or other.eventMask)
            
            return self.__class__(val, INT, vldMask, eventMask=eventMask)
        
        def __floordiv__(self, other):
            self._otherCheck(other)
            val = self.val // other.val
            vldMask = int(self.vldMask and other.vldMask)
            eventMask = int(self.eventMask or other.eventMask)

            return self.__class__(val, INT, vldMask, eventMask=eventMask)
        
        def __lt__(self, other):
            self._otherCheck(other)  
            val = self.val < other.val
            vldMask = int(self.vldMask and other.vldMask)
            eventMask = int(self.eventMask or other.eventMask)
            
            vCls = BOOL.ValueCls
            
            return vCls(val, BOOL, vldMask, eventMask=eventMask)

        def __gt__(self, other):
            self._otherCheck(other)  
            val = self.val > other.val
            vldMask = int(self.vldMask and other.vldMask)
            eventMask = int(self.eventMask or other.eventMask)
            
            vCls = BOOL.ValueCls
            
            return vCls(val, BOOL, vldMask, eventMask=eventMask)
            
    class ValueCls(Value, Ops):
        pass
        
class Std_logic(HdlType):
    """
    @ivar vldMask: can be only 0 or 1
    @ivar eventMask: can be only 0 or 1
    """
    def __init__(self):
        super(Std_logic, self).__init__()
        self.name = 'std_logic'
    
    def valAsVhdl(self, val, serializer):
        if val.vldMask:
            return  "'%d'" % int(bool(val.val))
        else:
            return "'X'"
    def convert(self, sigOrVal, toType):
        isVal = isinstance(sigOrVal, Value)
        
        if toType == BOOL:
            if isVal:
                return sigOrVal == Value.fromPyVal(1, BIT)
            else:
                v = 0 if sigOrVal.negated else 1
                return sigOrVal._eq(Value.fromPyVal(v, BIT))
        return super(Std_logic, self).convert(sigOrVal, toType)
            
    class Ops(TypeOps):
        @classmethod
        def fromPy(cls, val, typeObj):
            """
            @param val: value of python type int or None
            @param typeObj: instance of HdlType
            """
            vld = int(val is not None)
            if not vld:
                val = False
            assert(isinstance(val, int) or isinstance(val, bool))
            
            return cls(int(val), typeObj, vld)
        
        def _eq(self, other):
            if not isinstance(other, Value):
                raise AssertionError("%s _eq operator argument has to be instance of Value, is %s" % 
                                     (self.__class__.__name__ , repr(other)))
            
            vld = self.vldMask & other.vldMask
            eq = self.val == other.val and vld
            ev = self.eventMask | other.eventMask

            vCls = BOOL.ValueCls
            
            return vCls(eq, BOOL, vld, eventMask=ev)

    class ValueCls(Value, Ops):
        pass

class Std_logic_vector(HdlType):
    def __init__(self, signed=None):
        super(Std_logic_vector, self).__init__()
        if signed is None:
            self.name = 'std_logic_vector'
        elif signed:
            self.name = "signed"
        else:
            self.name = 'unsigned'
        self.signed = signed
        self.constrain = Unconstrained()
    
    def __call__(self, width, signed=None):
        return Std_logic_vector_contrained(width, signed=signed)
    
    def __eq__(self, other):
        return super().__eq__(other) and self.signed == other.signed
    
    def __hash__(self):
        return hash((self.name, self.signed, self.constrain))
    
    def convert(self, sigOrVal, toType):
        if sigOrVal._dtype == toType:
            return sigOrVal
        elif isinstance(toType, Integer):
            if isinstance(sigOrVal, Value):
                v = sigOrVal.clone()
                v._dtype = toType
                return v
        super(Std_logic_vector, self).convert(sigOrVal, toType)
            
    def valAsVhdl(self, val, serializer):
        c = self.constrain
        if isinstance(c, Unconstrained):
            width = [0, c.derivedWidth]
        elif isinstance(c, Value):
            width = [c.val[0].staticEval().val, c.val[1].staticEval().val]
        else:
            v = self.constrain.staticEval()
            width = [v.val[0].val, v.val[1].val]
        
        width = abs(width[1] - width[0]) + 1
        return serializer.BitString(val.val, width, val.vldMask)
    
    class Ops(TypeOps):
        @classmethod
        def fromPy(cls, val, typeObj):
            assert(val is None)
            v = VECTOR.ValueCls(0, VECTOR, 0, eventMask=0)
            return v 
        def getWidth(self):
            return self.width

    class ValueCls(Value, Ops):
        pass
 
class Std_logic_vector_contrained(Std_logic_vector):
    """
    Std_logic_vector with specified width
    """
    def __init__(self, widthConstr, signed=None):
        super(Std_logic_vector_contrained, self).__init__(signed=signed)
        self.constrain = widthConstr
        
    def __eq__(self, other):
        return super(Std_logic_vector_contrained, self).__eq__(other) \
                and (self.constrain == other.constrain or self.getBitCnt() == other.getBitCnt())
    def __hash__(self):
        return hash((self.name, self.signed, self.constrain))            
    def getBitCnt(self):
            return self.getWidth()
            
    def getWidth(self):
        w = self.constrain.staticEval()
         
        return abs(w.val[0].val - w.val[1].val) + 1
    
    def convert(self, sigOrVal, toType):
        if sigOrVal._dtype == toType:
            return sigOrVal
        elif type(toType) == Std_logic_vector:
            if isinstance(sigOrVal, Value):
                o = sigOrVal.clone()
                o._dtype = toType
                return o
        return super().convert(sigOrVal, toType)
       
    class Ops(Std_logic_vector.Ops):
        
        @classmethod
        def fromPy(cls, val, typeObj):
            assert(isinstance(val, int) or val is None)
            vld = 0 if val is None else Bitmask.mask(typeObj.getBitCnt())
            if not vld:
                val = 0
            return cls(val, typeObj, vld)
        
        def concat(self, other):
            from hdl_toolkit.synthetisator.rtlLevel.signal import SignalNode
            from hdl_toolkit.hdlObjects.operatorDefs import AllOps
            from hdl_toolkit.hdlObjects.operator import Operator
            v = self.clone()
            w = self._dtype.getBitCnt()
            v.val = (v.val << w) | other.val
            v.vldMask = (v.vldMask << w) | other.vldMask
            v.eventMask = (v.eventMask << w) | other.eventMask
            
            resWidth = w + other._dtype.getBitCnt()
            v._dtype = VECTOR(SignalNode.resForOp(
                                Operator(AllOps.DOWNTO, [ 
                                           Value.fromPyVal(resWidth - 1, INT),
                                           Value.fromPyVal(0, INT)])))
            return v
        
        def _eq(self, other):
            assert(isinstance(other, Value))
            w = self._dtype.getBitCnt()
            assert(w == other._dtype.getBitCnt())
            
            vld = self.vldMask & other.vldMask
            eq = self.val == other.val and vld == Bitmask.mask(w)
            ev = self.eventMask | other.eventMask

            vCls = BOOL.ValueCls
            
            return vCls(eq, BOOL, vld, eventMask=ev)
    
    class ValueCls(Value, Ops):
        pass
    
    def __repr__(self):
        from hdl_toolkit.synthetisator.vhdlSerializer import VhdlSerializer
        return "<HdlType %s, constrain:%s>" % (
            self.__class__.__name__, VhdlSerializer.asHdl(self.constrain))

def pushBit(v, b):
    return (v << 1) | b

class String(HdlType):
    def __init__(self):
        super(String, self).__init__()
        self.name = "string"

    def valAsVhdl(self, val, serializer):
        return  '"%s"' % str(val.val)
    def convert(self, sigOrVal, toType):
        if sigOrVal._dtype == toType:
            return sigOrVal
        elif toType == VECTOR:
            if isinstance(sigOrVal, Value):
                v = sigOrVal.clone()
                _v = v.val
                v.val = 0
                v.vldMask = 0
                v._dtype = toType
                for ch in reversed(_v): 
                    if ch == '1':
                        v.val = pushBit(v.val, 1)
                        v.vldMask = pushBit(v.vldMask, 1)
                    elif ch == '0':
                        v.val = pushBit(v.val, 0)
                        v.vldMask = pushBit(v.vldMask, 1)
                    elif ch == 'x':
                        v.val = pushBit(v.val, 0)
                        v.vldMask = pushBit(v.vldMask, 0)
                    else:
                        raise NotImplementedError("found %s in bitstring literal" % (ch))
                return v
                

    class Ops(TypeOps):
        @classmethod
        def fromPy(cls, val, typeObj):
            assert(isinstance(val, str) or val is None)
            vld = 0 if val is None else 1
            if not vld:
                val = ""
            return cls(val, typeObj, vld)
            
        def _eq(self, other):
            self._otherCheck(other)
            eq = self.val == other.val
            vld = int(self.vldMask and other.vldMask)
            ev = self.eventMask | other.eventMask
            vCls = BOOL.ValueCls
            
            return vCls(eq, STR, vld, eventMask=ev)

    class ValueCls(Value, Ops):
        pass

class Array(HdlType):
    """
    vldMask and eventMask on Array_val instance is not used instead of that
    these flags on elements are used
    [TODO] Array in Array
    [TODO] Array elements should always be instance of Signal
           to prevent problems in simulation
    """
    def __init__(self, elmType, size):
        super(Array, self).__init__()
        self.elmType = elmType
        self.size = size
    
    class Ops(TypeOps):
        @classmethod
        def fromPy(cls, val, typeObj):
            if val is None:
                val = [None for _ in range(typeObj.size)]
            assert(len(val) == typeObj.size)
            elements = []
            for v in val:
                if hasattr(v, "name"):  # is signal
                    assert(v._dtype == typeObj.elmType)
                    e = v
                else:   
                    e = Value.fromPyVal(v, typeObj.elmType)
                elements.append(e)
            
            
            return cls(elements, typeObj, 1)
        def _eq(self, other):
            assert(self._dtype.elmType == other._dtype.elmType)
            assert(self._dtype.size == other._dtype.size)
            
            eq = True
            first = self.val[0]
            vld = first.vldMask
            ev = first.eventMask
            
            for a, b in zip(self.val, other.val):
                eq = eq and a == b
                vld = vld & a.vldMask & b.vldMask
                ev = ev & a.eventMask & b.eventMask
            return BOOL.ValueCls(eq, BOOL, vld, eventMask=ev)

    class ValueCls(Value, Ops):
        pass            

class Positive(Integer):
    def __init__(self):
        super(Positive, self).__init__()
        self.name = "positive"

class Natural(Integer):
    def __init__(self):
        super(Natural, self).__init__()
        self.name = "natural"

class Range(Array):
    def __init__(self):
        super(Range, self).__init__(INT, 2)
        
    def valAsVhdl(self, val, serializer):
        return "%s DOWNTO %s" % (serializer.Value(val.val[0]), serializer.Value(val.val[1]))

    class Ops(Array.Ops):
        
        def staticEval(self):
            _0 = self.val[0].staticEval()
            _1 = self.val[0].staticEval()
            return Range.ValueCls([_0, _1], Range.ValueCls, vld=None, eventMask=None)
        
    class ValueCls(Array.ValueCls, Ops):
        pass
    
class Wire(Std_logic):
    """Verilog wire"""
    def __call__(self, width):
        return Std_logic_vector_contrained(width)

class Enum(HdlType):
    def __init__(self, name, valueNames):
        super(Enum, self).__init__()
        self.name = name
        self._allValues = valueNames
        for n in valueNames:
            setattr(self, n, Enum.ValueCls(n, self, 1, eventMask=0))
            
    def valAsVhdl(self, val, serializer):
        return  '%s' % str(val.val)
    
    class Ops(TypeOps):
        @classmethod
        def fromPy(cls, val, typeObj):
            """
            @param val: value of python type bool or None
            @param typeObj: instance of HdlType
            """
            if val is None:
                valid = False
                val = typeObj._allValues[0]
            else:
                valid = True
            assert(isinstance(val, str))
            
            return cls(val, typeObj, valid)
        
        def _eq(self, other):
            """return abs(w.val[0].val - w.val[1].val) + 1
        
            @attention: ignores eventMask
            """
            self._otherCheck(other)
    
            eq = self.val == other.val \
                and self.vldMask == other.vldMask == 1
            
            vldMask = int(self.vldMask == other.vldMask == 1)
            evMask = self.eventMask | other.eventMask
            return self.__class__(eq, BOOL, vldMask, eventMask=evMask)
    
    class ValueCls(Value, Ops):
        pass

def isInteger(t):
    isInt = False
    for _t in [INT, UINT, PINT]:
        if t == _t:
            isInt = True
    return isInt

def areIntegers(a, b):
    for t in [a, b]:
        if not isInteger(t):
            return False
    return True   


def getBitCnt(t):
    if t == BIT:
        return 1
    else:
        return t.getBitCnt()
              
      
BOOL = Boolean()
INT = Integer()
UINT = Natural()
PINT = Positive()
BIT = Std_logic()
VECTOR = Std_logic_vector()
STR = String()    
RANGE = Range()




