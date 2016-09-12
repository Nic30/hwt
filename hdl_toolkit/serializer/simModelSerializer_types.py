from hdl_toolkit.synthesizer.param import evalParam
from hdl_toolkit.hdlObjects.types.sliceVal import SliceVal
from hdl_toolkit.hdlObjects.types.bits import Bits
from hdl_toolkit.hdlObjects.types.enum import Enum
from hdl_toolkit.hdlObjects.types.array import Array
from hdl_toolkit.hdlObjects.types.hdlType import HdlType

class SimModelSerializer_types():
    @classmethod
    def HdlType_bits(cls, typ, declaration=False):
        if typ.signed is None:
            if not (typ.forceVector or typ.bit_length() > 1):
                return 'BIT'
            
        c = typ.constrain
        if isinstance(c, (int, float)):
            pass
        else:        
            c = evalParam(c)
            if isinstance(c, SliceVal):
                c = c._size()
            else:
                c = c.val  
             
        return "vecT(%d, %r)" % (c, typ.signed)

    @classmethod
    def HdlType_enum(cls, typ, scope, declaration=False):
        buff = []
        if declaration:
            try:
                name = typ.name
            except AttributeError:
                name = "enumT_"
            typ.name = scope.checkedName(name, typ)
            
            buff.extend(["TYPE ", typ.name.upper(), ' IS ('])
            # [TODO] check enum values names 
            buff.append(", ".join(typ._allValues))
            buff.append(")")
            return "".join(buff)
        else:
            return typ.name
        

    @classmethod
    def HdlType_array(cls, typ, scope, declaration=False):
        if declaration:
            try:
                name = typ.name
            except AttributeError:
                name = "arrT_"
            
            typ.name = scope.checkedName(name, typ)
            
            return "TYPE %s IS ARRAY ((%s) DOWNTO 0) OF %s" % \
                (typ.name, cls.asHdl(toHVal(typ.size) - 1), cls.HdlType(typ.elmType))
        else:
            try:
                return typ.name
            except AttributeError:
                # [TODO]
                # sometimes we need to debug expression and we need temporary type name
                # this may be risk and this should be done by extra debug serializer
                return "arrT_%d" % id(typ) 

    @classmethod
    def HdlType(cls, typ, scope=None, declaration=False):
        if isinstance(typ, Bits):
            return cls.HdlType_bits(typ, declaration=declaration)
        elif isinstance(typ, Enum):
            return cls.HdlType_enum(typ, scope, declaration=declaration)
        elif isinstance(typ, Array):
            return cls.HdlType_array(typ, scope, declaration=declaration)
        else:
            if declaration:
                raise NotImplementedError("type declaration is not implemented for type %s" % 
                                      (typ.name))
            else:
                assert isinstance(typ, HdlType)
                return typ.name.upper()
