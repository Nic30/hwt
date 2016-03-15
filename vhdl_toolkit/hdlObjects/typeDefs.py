from vhdl_toolkit.hdlObjects.types import HdlType
from vhdl_toolkit.hdlObjects.typeOps import TypeOps
from vhdl_toolkit.hdlObjects.specialValues import Unconstrained
from vhdl_toolkit.hdlObjects.value import Value
from vhdl_toolkit.bitmask import Bitmask
from vhdl_toolkit.synthetisator.exceptions import TypeConversionErr

class Boolean(HdlType):
    def __init__(self):
        super(Boolean, self).__init__()
        self.name = 'boolean'
    
    def valAsVhdl(self, val, serializer):
        return str(bool(val.val))
    
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
                
        def __eq__(self, other):
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
        if sigOrVal.dtype == toType:
            return sigOrVal
        elif toType == PINT:
            if isinstance(sigOrVal, Value):
                v = sigOrVal.clone()
                assert(v.val > 0)
                v.dtype = PINT
                return v
        elif toType == UINT:
            if isinstance(sigOrVal, Value):
                v = sigOrVal.clone()
                assert(v.val >= 0)
                v.dtype = UINT
                return v
            
                
        raise TypeConversionErr("Conversion of type %s to type %s is not implemented" % (repr(self), repr(toType)))
 
        
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
        
        def __eq__(self, other):
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
        return  "'%d'" % int(bool(val.val))
    
    def convert(self, sigOrVal, toType):
        isVal = isinstance(sigOrVal, Value)
        
        if toType == BOOL:
            if isVal:
                return sigOrVal == Value.fromPyVal(1, BIT)
            else:
                return sigOrVal.opEq(Value.fromPyVal(1, BIT))
        else:
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
        
        def __eq__(self, other):
            assert(isinstance(other, Value))
            
            vld = self.vldMask & other.vldMask
            eq = self.val == other.val and vld
            ev = self.eventMask | other.eventMask

            vCls = BOOL.ValueCls
            
            return vCls(eq, BOOL, vld, eventMask=ev)

    class ValueCls(Value, Ops):
        pass

class Std_logic_vector(HdlType):
    def __init__(self):
        super(Std_logic_vector, self).__init__()
        self.name = 'std_logic_vector'
        self.constrain = Unconstrained()
    
    def __call__(self, width):
        return Std_logic_vector_contrained(width)
    
    def valAsVhdl(self, val, serializer):
        c = self.constrain
        if isinstance(c, Unconstrained):
            width = [Value.fromPyVal(0, INT), Value.fromPyVal(c.derivedWidth, INT)]
        elif isinstance(c, Value):
            width = c.val
        else:
            width = self.constrain._staticEval()._val
        
        width = abs(width[1].val - width[0].val) + 1
        v = val.val
        if val.vldMask is None:
            if width % 4 == 0:
                return ('X"%0' + str(width % 4) + 'x"') % (v)
            else:
                return ('B"{0:0' + str(width) + 'b}"').format(v)
        else:
            raise NotImplementedError("vldMask not implemented yet")

    
    class Ops(TypeOps):

        def getWidth(self):
            return self.width

    class ValueCls(Value, Ops):
        pass
 
class Std_logic_vector_contrained(Std_logic_vector):
    """
    Std_logic_vector with specified width
    """
    def __init__(self, width):
        super(Std_logic_vector_contrained, self).__init__()
        self.name = 'std_logic_vector'
        self.constrain = width
    def __eq__(self, other):
        return super(Std_logic_vector_contrained, self).__eq__(other) \
                and self.constrain == other.constrain
    def getBitCnt(self):
            return self.getWidth()
        
    def getWidth(self):
        w = self.constrain
        if w.dtype == RANGE:
            pass
        else:
            w = w.staticEval()
            
        return abs(w.val[0].val - w.val[1].val) + 1
        
    class Ops(Std_logic_vector.Ops):
        
        @classmethod
        def fromPy(cls, val, typeObj):
            assert(isinstance(val, int) or val is None)
            vld = 0 if val is None else Bitmask.mask(typeObj.getBitCnt())
            if not vld:
                val = 0
            return cls(val, typeObj, vld)
        
        def __eq__(self, other):
            assert(isinstance(other, Value))
            w = self.dtype.getBitCnt()
            assert(w == other.dtype.getBitCnt())
            
            vld = self.vldMask & other.vldMask
            eq = self.val == other.val and vld == Bitmask.mask(w)
            ev = self.eventMask | other.eventMask

            vCls = BOOL.ValueCls
            
            return vCls(eq, BOOL, vld, eventMask=ev)
    
    class ValueCls(Value, Ops):
        pass

class String(HdlType):
    def __init__(self):
        super(String, self).__init__()
        self.name = "string"

    class Ops(TypeOps):
        @classmethod
        def fromPy(cls, val, typeObj):
            assert(isinstance(val, str) or val is None)
            vld = 0 if val is None else 1
            if not vld:
                val = ""
            return cls(val, typeObj, vld)
            
        def __eq__(self, other):
            self._otherCheck(other)
            eq = self.val == other.val
            vld = int(self.vldMask and other.vldMask)
            ev = self.eventMask | other.eventMask
            vCls = BOOL.ValueCls
            
            return vCls(eq, vCls, vld, eventMask=ev)

    class ValueCls(Value, Ops):
        pass

class Array(HdlType):
    """
    vldMask and eventMask on Array_val instance is not used instead of that
    these flags on elements are used
    [TODO] Array in Array
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
                    assert(v.dtype == typeObj.elmType)
                    e = v
                else:   
                    e = Value.fromPyVal(v, typeObj.elmType)
                elements.append(e)
            
            
            return cls(elements, typeObj, 1)
        def __eq__(self, other):
            assert(self.dtype.elmType == other.dtype.elmType)
            assert(self.dtype.size == other.dtype.size)
            vCls = BOOL.ValueCls
            
            eq = True
            first = self.val[0]
            vld = first.vldMask
            ev = first.eventMask
            
            for a, b in zip(self.val, other.val):
                eq = eq and a == b
                vld = vld & a.vldMask & b.vldMask
                ev = ev & a.eventMask & b.eventMask
            return vCls(eq, vCls, vld, eventMask=ev)

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

    
     
BOOL = Boolean()
INT = Integer()
UINT = Natural()
PINT = Positive()
BIT = Std_logic()
VECTOR = Std_logic_vector()
STR = String()    
RANGE = Range()
