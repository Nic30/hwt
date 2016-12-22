from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.boolean import Boolean
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.string import String
from hwt.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hwt.hdlObjects.types.slice import Slice
from hwt.synthesizer.param import Param, evalParam


class SimModelSerializer_value():
        
    @classmethod
    def Bits_valAsVhdl(cls, dtype, val):
        return "BitsVal(%d, simBitsT(%d, %r), %d)" % (
            val.val, dtype.bit_length(), dtype.signed, val.vldMask)
   
    @classmethod
    def SignalItem(cls, si, declaration=False):
        if declaration:
            raise NotImplementedError()
        else:
            if isinstance(si, Param):
                return cls.Value(evalParam(si))
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin)
            else:
                return "self.%s._oldVal" % si.name
    @classmethod
    def Integer_valAsVhdl(cls, t, i):
        if i.vldMask:
            return "simHInt(%d)" % i.val
        else:
            return "simHInt(None)"
    
    @classmethod
    def Array_valAsVhdl(cls, t, val):
        return "ArrayVal([%s], %s, %d)" % (",\n".join(map(cls.Value, val.val)), cls.HdlType(t), val.vldMask)
    
    @classmethod
    def Slice_valAsVhdl(cls, t, val):
        return "SliceVal((simHInt(%d), simHInt(%d)), SLICE, %d)" % (evalParam(val.val[0]).val, evalParam(val.val[1]).val,
                                                  val.vldMask)
    @classmethod
    def Enum_valAsVhdl(cls, t, val):
        return "self.%s.%s" % (t.name, val.val)
    
    
    @classmethod
    def Value(cls, val):
        """ 
        @param dst: is signal connected with value 
        @param val: value object, can be instance of Signal or Value    """
        t = val._dtype
        
        if isinstance(val, RtlSignalBase):
            return cls.SignalItem(val)
        elif isinstance(t, Slice):
            return cls.Slice_valAsVhdl(t, val)
        elif isinstance(t, Array):
            return cls.Array_valAsVhdl(t, val)
        elif isinstance(t, Bits):
            return cls.Bits_valAsVhdl(t, val)
        elif isinstance(t, Boolean):
            return cls.Bool_valAsVhdl(t, val)
        elif isinstance(t, Enum):
            return cls.Enum_valAsVhdl(t, val)
        elif isinstance(t, Integer):
            return cls.Integer_valAsVhdl(t, val)
        elif isinstance(t, String):
            return cls.String_valAsVhdl(t, val)
        else:
            raise Exception("value2vhdlformat can not resolve value serialization for %s" % (repr(val))) 
    
