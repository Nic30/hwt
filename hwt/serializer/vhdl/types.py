from hwt.hdlObjects.constants import Unconstrained
from hwt.hdlObjects.types.hdlType import HdlType
from hwt.hdlObjects.types.array import Array
from hwt.hdlObjects.types.bits import Bits
from hwt.hdlObjects.types.enum import Enum
from hwt.hdlObjects.types.integer import Integer
from hwt.hdlObjects.types.typeCast import toHVal
from hwt.serializer.exceptions import SerializerException


class VhdlSerializer_types():
    @classmethod
    def HdlType_bits(cls, typ, createTmpVarFn, declaration=False):
        disableRange = False
        if typ.signed is None:
            if typ.forceVector or typ.bit_length() > 1:
                name = 'STD_LOGIC_VECTOR'
            else:
                name = 'STD_LOGIC'
                disableRange = True
        elif typ.signed:
            name = "SIGNED"
        else:
            name = 'UNSIGNED'     
            
        c = typ.constrain
        if disableRange or c is None or isinstance(c, Unconstrained):
            constr = ""
        elif isinstance(c, (int, float)):
            constr = "(%d DOWNTO 0)" % (c - 1)
        else:        
            constr = "(%s)" % cls.Value(c, createTmpVarFn)     
        return name + constr


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
    def HdlType_array(cls, typ, createTmpVarFn, scope, declaration=False):
        if declaration:
            try:
                name = typ.name
            except AttributeError:
                name = "arrT_"
            
            typ.name = scope.checkedName(name, typ)
            
            return "TYPE %s IS ARRAY ((%s) DOWNTO 0) OF %s" % \
                (typ.name, cls.asHdl(toHVal(typ.size) - 1, createTmpVarFn), cls.HdlType(typ.elmType, createTmpVarFn))
        else:
            try:
                return typ.name
            except AttributeError:
                # [TODO]
                # sometimes we need to debug expression and we need temporary type name
                # this may be risk and this should be done by extra debug serializer
                return "arrT_%d" % id(typ) 
    
    @classmethod
    def HdlType_int(cls, typ, scope, declaration=False):
        ma = typ.max
        mi = typ.min
        noMax = ma is None
        noMin = mi is None
        if noMin: 
            if noMax:
                return "INTEGER"
            else:
                raise SerializerException("If max is specified min has to be specified as well")
        else:
            if noMax:
                if mi == 0:
                    return "NATURAL"
                elif mi == 1:
                    return "POSITIVE"
                else:
                    raise SerializerException("If max is specified min has to be specified as well")
            else:
                return "INTEGER RANGE %d to %d" % (mi, ma)
    
    @classmethod
    def HdlType(cls, typ, createTmpVarFn, scope=None, declaration=False):
        if isinstance(typ, Bits):
            return cls.HdlType_bits(typ, createTmpVarFn, declaration=declaration)
        elif isinstance(typ, Enum):
            return cls.HdlType_enum(typ, scope, declaration=declaration)
        elif isinstance(typ, Array):
            return cls.HdlType_array(typ, createTmpVarFn, scope, declaration=declaration)
        elif isinstance(typ, Integer):
            return cls.HdlType_int(typ, scope, declaration=declaration)
        else:
            if declaration:
                raise NotImplementedError("type declaration is not implemented for type %s" % 
                                      (typ.name))
            else:
                assert isinstance(typ, HdlType)
                return typ.name.upper()
