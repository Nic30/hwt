from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.boolean import Boolean
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.hdlObjects.types.integer import Integer
from hdl_toolkit.hdlObjects.types.string import String
from hdl_toolkit.synthesizer.rtlLevel.mainBases import RtlSignalBase
from hdl_toolkit.hdlObjects.types.slice import Slice
from hdl_toolkit.bitmask import Bitmask
from hdl_toolkit.serializer.exceptions import SerializerException
from hdl_toolkit.hdlObjects.value import Value


class SimModelSerializer_value():
        
    @classmethod
    def Bits_valAsVhdl(cls, dtype, val):
        return "vec(, )"
   
    @staticmethod
    def BitString_binary(v, width, vldMask=None):
        buff = []
        for i in range(width - 1, -1, -1):
            mask = (1 << i)
            b = v & mask
            
            if vldMask & mask:
                s = "1" if b else "0"
            else:
                s = "X"
            buff.append(s)
        return '"%s"' % (''.join(buff))

    @classmethod
    def BitString(cls, v, width, vldMask=None):
        if vldMask is None:
            vldMask = Bitmask.mask(width)
        # if can be in hex
        if width % 4 == 0 and vldMask == (1 << width) - 1:
            return ('X"%0' + str(width // 4) + 'x"') % (v)
        else:  # else in binary
            return cls.BitString_binary(v, width, vldMask)
    
    @classmethod
    def BitLiteral(cls, v, vldMask):
        if vldMask:
            return  "'%d'" % int(bool(v))
        else:
            return "'X'"
    
    @classmethod
    def SignedBitString(cls, v, width, vldMask):
        if vldMask != Bitmask.mask(width):
            raise SerializerException(
            "Value %s can not be serialized as signed bit string literal due not all bits are valid" % 
             repr(v))
        else:
            # [TODO] parametrized width
            return "TO_SIGNED(%d, %d)" % (v, width)

    @classmethod
    def UnsignedBitString(cls, v, width, vldMask):
        if vldMask != Bitmask.mask(width):
            raise SerializerException(
            "Value %s can not be serialized as signed bit string literal due not all bits are valid" % 
             repr(v))
        else:
            # [TODO] parametrized width
            return "TO_UNSIGNED(%d, %d)" % (v, width)

    @classmethod
    def SignalItem(cls, si, declaration=False):
        if declaration:
            if si.drivers:
                prefix = "SIGNAL"
            elif si.endpoints or si.simSensitiveProcesses:
                prefix = "CONSTANT"
            else:
                raise SerializerException("Signal %s should be declared but it is not used" % si.name)
                

            s = prefix + " %s : %s" % (si.name, cls.HdlType(si._dtype))
            if si.defaultVal is not None:
                v = si.defaultVal
                if isinstance(v, RtlSignalBase):
                    return s + " := %s" % cls.asHdl(v)
                elif isinstance(v, Value):
                    if si.defaultVal.vldMask:
                        return s + " := %s" % cls.Value(si.defaultVal)
                else:
                    raise NotImplementedError(v)
                
            return s 
        else:
            if si.hidden and hasattr(si, "origin"):
                return cls.asHdl(si.origin)
            else:
                return "self.%s._oldVal" % si.name

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
    