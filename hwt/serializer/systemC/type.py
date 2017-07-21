from hwt.hdlObjects.types.bits import Bits


class SystemCSerializer_type():
    @classmethod
    def HdlType_bits(cls, typ, ctx, declaration=False):
        if declaration:
            raise NotImplementedError()
        
        w = typ.bit_length()
        
        if w <= 64:
            if typ.signed:
                typeBaseName = "int" 
            else:
                typeBaseName = "uint"
        else:
            if typ.signed:
                typeBaseName = "bigint" 
            else:
                typeBaseName = "biguint"
            
        return "sc_%s<%d>" % (typeBaseName, w)
    
    @classmethod
    def HdlType_enum(cls, typ, ctx, declaration=False):
        if declaration:
            raise TypeError("There is problem with tracing of c enums, use Bits instead")
        else:
            valueCnt = len(typ._allValues)
            return cls.HdlType_bits(Bits(valueCnt.bit_length()), ctx, declaration=declaration)